import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, ttest_ind

# ============ Load results.jsonl ============
def load_results(file_path="data/results.jsonl"):
    rows = []
    with open(file_path, "r") as f:
        for line in f:
            data = json.loads(line)

            # Safely handle OpenAI & Perspective outputs
            openai_scores = data.get("openai", {}).get("category_scores", {})
            persp_scores = {
                k: v["summaryScore"]["value"]
                for k, v in data.get("perspective", {}).get("attributeScores", {}).items()
            }

            rows.append({
                "post_id": data.get("post_id"),
                "text": data.get("text"),
                "openai_flagged": data.get("openai", {}).get("flagged", False),
                "persp_toxicity": persp_scores.get("TOXICITY", None),
                **{f"oa_{k}": v for k, v in openai_scores.items()},
                **{f"persp_{k.lower()}": v for k, v in persp_scores.items()}
            })
    return pd.DataFrame(rows)


# ============ Analysis Functions ============
def correlation_analysis(df):
    if "oa_violence" in df and "persp_toxicity" in df:
        corr, _ = pearsonr(df["oa_violence"], df["persp_toxicity"])
        print(f"🔗 Correlation (OpenAI violence vs Perspective toxicity): {corr:.3f}")
    else:
        print("⚠️ Missing columns for correlation analysis")


def agreement_analysis(df, threshold=0.5):
    df["openai_label"] = df["oa_violence"] > threshold
    df["persp_label"] = df["persp_toxicity"] > threshold
    agreement = (df["openai_label"] == df["persp_label"]).mean()
    print(f"✅ Agreement between APIs: {agreement*100:.2f}%")


def category_distribution(df):
    oa_cols = [c for c in df.columns if c.startswith("oa_")]
    mean_scores = df[oa_cols].mean().sort_values(ascending=False)

    plt.figure(figsize=(12, 5))
    sns.barplot(x=mean_scores.index, y=mean_scores.values, palette="viridis", legend=False)
    plt.title("Average OpenAI Category Scores", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Mean Score")
    plt.tight_layout()
    plt.show()


def statistical_test(df, threshold=0.5):
    df["openai_label"] = df["oa_violence"] > threshold
    df["persp_label"] = df["persp_toxicity"] > threshold
    tstat, pval = ttest_ind(df["openai_label"], df["persp_label"])
    print(f"📊 T-test between APIs: t={tstat:.3f}, p={pval:.3f}")


def visualize(df):
    if "oa_violence" in df and "persp_toxicity" in df:
        plt.figure(figsize=(7, 5))
        sns.scatterplot(x="oa_violence", y="persp_toxicity", data=df, alpha=0.6, edgecolor=None)
        plt.title("OpenAI Violence vs Perspective Toxicity")
        plt.xlabel("OpenAI Violence Score")
        plt.ylabel("Perspective Toxicity Score")
        plt.tight_layout()
        plt.show()
    else:
        print("⚠️ Missing columns for visualization")


# ============ New: Disagreement Analysis ============
def disagreement_analysis(df, threshold=0.5):
    df["openai_label"] = df["oa_violence"] > threshold
    df["persp_label"] = df["persp_toxicity"] > threshold

    disagreements = df[df["openai_label"] != df["persp_label"]]
    print(f"⚠️ Disagreements found: {len(disagreements)} out of {len(df)} ({100*len(disagreements)/len(df):.2f}%)")

    # Look at average OpenAI scores in disagreement cases
    oa_cols = [c for c in df.columns if c.startswith("oa_")]
    mean_disagreement = disagreements[oa_cols].mean().sort_values(ascending=False)

    plt.figure(figsize=(12, 5))
    sns.barplot(x=mean_disagreement.index, y=mean_disagreement.values, palette="magma", legend=False)
    plt.title("Average OpenAI Category Scores (Disagreement Cases)", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Mean Score")
    plt.tight_layout()
    plt.show()


# ============ Run Full Analysis ============
if __name__ == "__main__":
    df = load_results("data/results.jsonl")
    print("✅ Data loaded:", df.shape)

    correlation_analysis(df)
    agreement_analysis(df)
    category_distribution(df)
    statistical_test(df)
    visualize(df)
    disagreement_analysis(df)   # << NEW
