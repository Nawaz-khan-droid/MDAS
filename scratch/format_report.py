import json

def generate_report():
    try:
        with open("scratch/dataset_report.json") as f:
            datasets = json.load(f)
        with open("scratch/benchmark_results.json") as f:
            benchmarks = json.load(f)
    except FileNotFoundError:
        print("Run the benchmark first.")
        return

    report = ["# Phase 1: Dataset & Benchmark Report\n\n"]
    
    report.append("## Dataset Audit\n\n")
    for task, data in datasets.items():
        if data.get("status") == "error":
            report.append(f"### {task.upper()}\n- **Status**: ERROR\n- **Reason**: {data.get('reason')}\n\n")
            continue
            
        report.append(f"### {task.upper()}\n")
        report.append(f"- **Rows**: {data['rows']}\n")
        report.append(f"- **Classes**: {data['classes']}\n")
        report.append(f"- **Minimum Class Count**: {data['min_class_count']}\n")
        
        dist_str = ", ".join([f"{k}: {v}" for k, v in data['distribution'].items()])
        report.append(f"- **Distribution**: {dist_str}\n")
        
        status_icon = "✅" if data['status'] == "viable" else ("⚠️" if data['status'] == "experimental" else "❌")
        report.append(f"- **Status**: {status_icon} {data['status']} (Reason: {data.get('reason', 'N/A')})\n\n")

    report.append("---\n\n## Benchmark Results (Viable Tasks)\n\n")
    
    for task, results in benchmarks.items():
        report.append(f"### Task: {task.upper()}\n\n")
        report.append("| Rank | Candidate | Macro F1 | Weighted F1 | Accuracy | Latency/Sample | CV Time (5 folds) |\n")
        report.append("|------|-----------|----------|-------------|----------|----------------|-------------------|\n")
        
        for i, r in enumerate(results, 1):
            name = r['candidate']
            mf1 = r['macro_f1']
            wf1 = r['weighted_f1']
            acc = r['accuracy']
            lat = f"{r['latency_sec_per_sample']:.5f}s"
            t_total = f"{r['cv_time_sec']}s"
            
            icon = "🏆" if i == 1 else ""
            report.append(f"| {i} {icon} | {name} | **{mf1}** | {wf1} | {acc} | {lat} | {t_total} |\n")
            
        report.append("\n")

    with open("scratch/benchmark_report.md", "w", encoding="utf-8") as f:
        f.writelines(report)
        
    print("Generated scratch/benchmark_report.md")

if __name__ == "__main__":
    generate_report()
