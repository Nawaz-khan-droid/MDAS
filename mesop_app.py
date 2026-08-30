import time
import json
import urllib.parse
from dataclasses import asdict, dataclass, field
from typing import Callable, Literal

import mesop as me
from mdas import MDASAnalyzer

# Initialize Backend
analyzer = MDASAnalyzer.from_directory("models")

_APP_TITLE = "MDAS Analytics"
_CHAT_MAX_WIDTH = "1000px"

@dataclass
class Tab:
  label: str
  content: Callable
  selected: bool = False
  icon: str | None = None


@me.stateclass
class State:
  input_text: str = ""
  in_progress: bool = False
  sidebar_expanded: bool = True
  selected_tab_index: int = 0
  
  # The currently active analysis
  active_text: str = ""
  active_result: str = "{}"  # serialized JSON dict to avoid state issues
  
  # History of past analyses (list of dicts containing text and result)
  history: list[str] = field(default_factory=list)


def on_load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  title="MDAS Mesop Dashboard",
  path="/",
  on_load=on_load,
)
def page():
  state = me.state(State)

  with me.box(
    style=me.Style(
      background=me.theme_var("surface-container-lowest"),
      display="flex",
      flex_direction="row",
      height="100vh",
      overflow="hidden"
    )
  ):
    # 1. Left Sidebar (History)
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container-low"),
        display="flex",
        flex_direction="column",
        flex_shrink=0,
        height="100%",
        width=300 if state.sidebar_expanded else 70,
        transition="width 0.2s ease",
        border=me.Border(right=me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant")))
      )
    ):
      sidebar()

    # 2. Middle Pane (Dashboard & Input)
    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="column",
        flex_grow=1,
        flex_basis="0",
        border=me.Border(right=me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant")))
      )
    ):
      header()
      with me.box(style=me.Style(flex_grow=1, overflow_y="auto", padding=me.Padding.all(20))):
        if state.active_text:
          dashboard_pane()
        else:
          empty_state()
      chat_input()

    # 3. Right Pane (Code Preview)
    with me.box(
      style=me.Style(
        display="flex",
        flex_direction="column",
        flex_shrink=0,
        width="35%",
        background=me.theme_var("surface-container-lowest")
      )
    ):
      code_preview_pane()


# ==========================================
# SIDEBAR
# ==========================================
def sidebar():
  state = me.state(State)
  with me.box(style=me.Style(display="flex", flex_direction="column", flex_grow=1)):
    with me.box(style=me.Style(display="flex", align_items="center", gap=10, padding=me.Padding.all(10))):
      icon_button(icon="menu", tooltip="Toggle Menu", on_click=on_click_menu_icon)
      if state.sidebar_expanded:
        me.text("MDAS", style=me.Style(margin=me.Margin(bottom=0), font_weight="bold"), type="headline-6")

    if state.sidebar_expanded:
      with me.box(style=me.Style(padding=me.Padding.symmetric(horizontal=10, vertical=10))):
        me.button(label="New Analysis", on_click=on_click_new_analysis, type="flat", style=me.Style(width="100%"))

      # History List
      with me.box(style=me.Style(flex_grow=1, overflow_y="auto")):
        for index, item_json in enumerate(state.history):
          item = json.loads(item_json)
          with me.box(
            key=f"history-{index}",
            on_click=on_click_history,
            style=me.Style(
              background=me.theme_var("surface-container-high") if item["text"] == state.active_text else "transparent",
              border_radius=8,
              cursor="pointer",
              margin=me.Margin.symmetric(horizontal=10, vertical=5),
              padding=me.Padding.all(12),
              text_overflow="ellipsis",
              white_space="nowrap",
              overflow="hidden"
            ),
          ):
            me.text(_truncate_text(item["text"], 30))
    else:
      with me.box(style=me.Style(display="flex", justify_content="center", margin=me.Margin(top=10))):
        icon_button(icon="add", tooltip="New Analysis", on_click=on_click_new_analysis)


# ==========================================
# MIDDLE PANE (DASHBOARD)
# ==========================================
def header():
  state = me.state(State)
  with me.box(
    style=me.Style(
      align_items="center",
      background=me.theme_var("surface-container-lowest"),
      display="flex",
      justify_content="space-between",
      padding=me.Padding.symmetric(horizontal=20, vertical=15),
      border=me.Border(bottom=me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant")))
    )
  ):
    me.text(_APP_TITLE, style=me.Style(margin=me.Margin(bottom=0)), type="headline-6")
    icon_button(
      icon="dark_mode" if me.theme_brightness() == "light" else "light_mode",
      tooltip="Toggle Theme",
      on_click=on_click_theme_brightness,
    )


def empty_state():
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      align_items="center",
      justify_content="center",
      height="100%",
      color=me.theme_var("on-surface-variant")
    )
  ):
    me.icon("analytics", style=me.Style(font_size=64, margin=me.Margin(bottom=20)))
    me.text("Enter a message below to start multi-dimensional analysis.", type="headline-6")


def dashboard_pane():
  state = me.state(State)
  if not state.active_result or state.active_result == "{}":
      return
      
  res = json.loads(state.active_result)
  radar = res.get("radar", {})
  classification = res.get("classification", {})
  
  with me.box(style=me.Style(display="flex", flex_direction="column", gap=20)):
    # Payload Text
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container"),
        border_radius=12,
        padding=me.Padding.all(20)
      )
    ):
      me.text("Analyzed Text", style=me.Style(font_weight="bold", color=me.theme_var("primary"), margin=me.Margin(bottom=10)))
      me.text(state.active_text, style=me.Style(font_size=16, line_height="1.5"))

    # KPI Grid
    with me.box(
      style=me.Style(
        display="grid",
        grid_template_columns="repeat(auto-fit, minmax(150px, 1fr))",
        gap=15
      )
    ):
      kpi_card("Sentiment", radar.get("sentiment", 0), is_percent=False)
      kpi_card("Urgency", radar.get("urgency", 0), is_percent=True)
      kpi_card("Churn Risk", radar.get("churn_risk", 0), is_percent=True)
      kpi_card("Toxicity", radar.get("toxicity", 0), is_percent=True)
      kpi_card("Sarcasm", radar.get("sarcasm", 0), is_percent=True)
      
    # Classification Results
    with me.box(
      style=me.Style(
        background=me.theme_var("surface-container-low"),
        border_radius=12,
        padding=me.Padding.all(20),
        margin=me.Margin(top=10)
      )
    ):
      me.text("Classification Details", style=me.Style(font_weight="bold", margin=me.Margin(bottom=15)))
      for key, val in classification.items():
          label = val.get("label", "Unknown")
          conf = val.get("confidence", 0)
          with me.box(style=me.Style(display="flex", justify_content="space-between", border=me.Border(bottom=me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant"))), padding=me.Padding.symmetric(vertical=8))):
              me.text(key.capitalize(), style=me.Style(font_weight="500"))
              me.text(f"{label} ({conf*100:.1f}%)")


def kpi_card(title: str, value: float, is_percent: bool):
  val_str = f"{value * 100:.1f}%" if is_percent else f"{value:.2f}"
  with me.box(
    style=me.Style(
      background=me.theme_var("surface-container-low"),
      border_radius=12,
      padding=me.Padding.all(15),
      display="flex",
      flex_direction="column",
      align_items="center",
      border=me.Border.all(me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant")))
    )
  ):
    me.text(title, style=me.Style(font_size=12, color=me.theme_var("on-surface-variant"), text_transform="uppercase"))
    me.text(val_str, style=me.Style(font_size=24, font_weight="bold", margin=me.Margin(top=10)))


def chat_input():
  state = me.state(State)
  with me.box(
    style=me.Style(
      background=me.theme_var("surface-container"),
      display="flex",
      padding=me.Padding.all(20),
      border=me.Border(top=me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant")))
    )
  ):
    with me.box(
      style=me.Style(
        flex_grow=1,
        background=me.theme_var("surface-container-highest"),
        border_radius=24,
        display="flex",
        align_items="center",
        padding=me.Padding.symmetric(horizontal=15, vertical=5)
      )
    ):
      with me.box(style=me.Style(flex_grow=1)):
        me.native_textarea(
          autosize=True,
          key="chat_input",
          min_rows=1,
          on_blur=on_chat_input,
          shortcuts={
            me.Shortcut(shift=False, key="Enter"): on_submit_chat_msg,
          },
          placeholder="Type a message to analyze...",
          style=me.Style(
            background="transparent",
            border=me.Border.all(me.BorderSide(style="none")),
            color=me.theme_var("on-surface"),
            outline="none",
            width="100%",
            padding=me.Padding(top=12, bottom=12),
            font_size=15
          ),
          value=state.input_text,
        )
      with me.content_button(
        disabled=state.in_progress,
        on_click=on_click_submit_chat_msg,
        type="icon",
      ):
        me.icon("send", style=me.Style(color=me.theme_var("primary")))


# ==========================================
# RIGHT PANE (CODE TABS)
# ==========================================
def code_preview_pane():
  state = me.state(State)
  
  tabs = [
    Tab(label="Python", content=lambda: render_code(get_python_code()), icon="code"),
    Tab(label="REST", content=lambda: render_code(get_rest_code()), icon="api"),
    Tab(label="JSON", content=lambda: render_code(get_json_code(), lang="json"), icon="data_object"),
  ]
  
  # Tab Header
  with me.box(
    style=me.Style(
      display="flex",
      width="100%",
      border=me.Border(bottom=me.BorderSide(width=1, style="solid", color=me.theme_var("outline-variant")))
    )
  ):
    for index, tab in enumerate(tabs):
      selected = state.selected_tab_index == index
      with me.box(
        key=f"tab-{index}",
        on_click=on_tab_click,
        style=me.Style(
          align_items="center",
          color=me.theme_var("on-surface"),
          display="flex",
          cursor="pointer",
          flex_grow=1,
          justify_content="center",
          font_size=14,
          font_weight="medium",
          padding=me.Padding.all(15),
          gap=5,
          background=me.theme_var("surface-container") if selected else "transparent",
          border=me.Border(bottom=me.BorderSide(width=2, style="solid", color=me.theme_var("primary"))) if selected else None
        )
      ):
        if tab.icon:
          me.icon(tab.icon, style=me.Style(font_size=18))
        me.text(tab.label)
        
  # Tab Content
  with me.box(style=me.Style(flex_grow=1, overflow_y="auto", padding=me.Padding.all(15), background=me.theme_var("surface-container-lowest"))):
    for index, tab in enumerate(tabs):
      if state.selected_tab_index == index:
        tab.content()


def render_code(code: str, lang: str = "python"):
  me.markdown(f"```{lang}\n{code}\n```")


def get_python_code():
  state = me.state(State)
  text = state.active_text or "URGENT: System is down!"
  escaped = text.replace('"', '\\"')
  return f'''# --- MDAS Python SDK ---
from mdas import MDASAnalyzer

analyzer = MDASAnalyzer.from_directory("models")

result = analyzer.analyze("{escaped}")

print(result.to_dict())
'''

def get_rest_code():
  state = me.state(State)
  text = state.active_text or "URGENT: System is down!"
  escaped = text.replace('"', '\\"')
  return f'''# --- Keyless REST API ---
curl -X POST "http://localhost:8000/api/analyze" \\
     -H "Content-Type: application/json" \\
     -d '{{"text": "{escaped}"}}'
'''

def get_json_code():
  state = me.state(State)
  if state.active_result and state.active_result != "{}":
      try:
          return json.dumps(json.loads(state.active_result), indent=2)
      except:
          pass
  return '{\n  "status": "waiting_for_input"\n}'


# ==========================================
# EVENT HANDLERS
# ==========================================
def on_click_menu_icon(e: me.ClickEvent):
  state = me.state(State)
  state.sidebar_expanded = not state.sidebar_expanded

def on_click_theme_brightness(e: me.ClickEvent):
  if me.theme_brightness() == "light":
    me.set_theme_mode("dark")
  else:
    me.set_theme_mode("light")

def on_chat_input(e: me.InputBlurEvent):
  state = me.state(State)
  state.input_text = e.value

def on_submit_chat_msg(e: me.TextareaShortcutEvent):
  state = me.state(State)
  state.input_text = e.value
  yield from _run_analysis()

def on_click_submit_chat_msg(e: me.ClickEvent):
  yield from _run_analysis()

def _run_analysis():
  state = me.state(State)
  if state.in_progress or not state.input_text.strip():
    return
    
  text_to_analyze = state.input_text.strip()
  state.input_text = ""
  state.in_progress = True
  yield
  
  # Run the actual ML model inference
  try:
    result = analyzer.analyze(text_to_analyze)
    res_dict = result.to_dict()
  except Exception as e:
    res_dict = {"error": str(e)}
    
  state.active_text = text_to_analyze
  state.active_result = json.dumps(res_dict)
  
  # Save to history
  state.history.insert(0, json.dumps({"text": text_to_analyze, "result": res_dict}))
  
  state.in_progress = False
  me.focus_component(key="chat_input")
  yield

def on_click_history(e: me.ClickEvent):
  state = me.state(State)
  _, idx = e.key.split("-")
  item = json.loads(state.history[int(idx)])
  state.active_text = item["text"]
  state.active_result = json.dumps(item["result"])
  
def on_click_new_analysis(e: me.ClickEvent):
  state = me.state(State)
  state.active_text = ""
  state.active_result = "{}"
  me.focus_component(key="chat_input")

def on_tab_click(e: me.ClickEvent):
  state = me.state(State)
  _, tab_index = e.key.split("-")
  state.selected_tab_index = int(tab_index)


# ==========================================
# HELPERS
# ==========================================
def icon_button(*, icon: str, tooltip: str, on_click: Callable):
  with me.tooltip(message=tooltip):
    with me.content_button(type="icon", on_click=on_click):
      me.icon(icon)

def _truncate_text(text: str, limit: int = 50) -> str:
  if len(text) <= limit:
    return text
  return text[:limit] + "..."
