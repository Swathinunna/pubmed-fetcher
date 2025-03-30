import argparse
from Bio import Entrez, Medline
import pandas as pd

# Set your PubMed API email
Entrez.email = "your-email@example.com"  # Change to your email

def fetch_pubmed_papers(query: str, max_results: int = 10, debug: bool = False) -> list:
    """Fetches research papers from PubMed based on a given query."""
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        paper_ids = record.get("IdList", [])

        if debug:
            print(f"Query: {query}, Max Results: {max_results}, Paper IDs: {paper_ids}")

        return paper_ids

    except Exception as e:
        print("Error fetching PubMed papers:", e)
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch PubMed papers")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-m", "--max_results", type=int, default=10, help="Maximum number of results to fetch")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    results = fetch_pubmed_papers(args.query, args.max_results, args.debug)

    if results:
        print(f"Found {len(results)} papers for '{args.query}'.")
        df = pd.DataFrame(results, columns=["PMID"])
        df.to_csv("pubmed_results.csv", index=False)
        print("Results saved to pubmed_results.csv")
    else:
        print("No matching papers found.")
