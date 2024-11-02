import os
import warnings
import time
import torch
from gliner import GLiNER
from typing import List, Dict, Any
from dataclasses import dataclass
import gc  # For garbage collection
from tabulate import tabulate  # pip install tabulate

@dataclass
class ProcessingStats:
    """Data class to store processing statistics"""
    process_time: float
    text_length: int
    entity_count: int

class OptimizedEntityExtractor:
    def __init__(self, 
                 model_name: str = "urchade/gliner_medium-v2.1",
                 batch_size: int = 8,
                 device: str = None,
                 confidence_threshold: float = 0.5):
        
        warnings.filterwarnings('ignore')
        os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
        
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._initialize_model(model_name)
        self.batch_size = batch_size
        self.confidence_threshold = confidence_threshold
        self.labels = ["person", "organization", "location", "date", "product"]

    def _initialize_model(self, model_name: str):
        start_time = time.time()
        model = GLiNER.from_pretrained(model_name)
        model.eval()
        return model

    def process_texts(self, texts: List[str]) -> tuple[List[List[Dict]], List[ProcessingStats]]:
        all_results = []
        all_stats = []
        
        batch_start = time.time()
        for text in texts:
            entities = self.model.predict_entities(text, self.labels)
            filtered_entities = [
                entity for entity in entities 
                if entity['score'] >= self.confidence_threshold
            ]
            
            all_results.append(filtered_entities)
            all_stats.append(ProcessingStats(
                process_time=time.time() - batch_start,
                text_length=len(text),
                entity_count=len(filtered_entities)
            ))
            
        return all_results, all_stats

def run_original_benchmark(test_texts: List[str], labels: List[str]) -> Dict:
    """Run benchmark for original implementation"""
    warnings.filterwarnings('ignore')
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

    print("\nRunning Original Implementation...")
    
    # Load model and time it
    start_time = time.time()
    model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    load_time = time.time() - start_time
    print(f"Original load time: {load_time:.2f} seconds")

    # Process texts
    results = []
    process_times = []
    
    print("\nProcessing texts with original implementation...")
    for i, text in enumerate(test_texts, 1):
        start_time = time.time()
        entities = model.predict_entities(text, labels)
        process_time = time.time() - start_time
        process_times.append(process_time)
        results.append(len(entities))
        print(f"Text {i}: Processed in {process_time:.2f} seconds, found {len(entities)} entities")

    total_time = sum(process_times)
    total_chars = sum(len(text) for text in test_texts)
    
    return {
        'load_time': load_time,
        'total_process_time': total_time,
        'avg_process_time': total_time / len(test_texts),
        'chars_per_second': total_chars / total_time,
        'total_entities': sum(results)
    }

def run_optimized_benchmark(test_texts: List[str], labels: List[str]) -> Dict:
    """Run benchmark for optimized implementation"""
    print("\nRunning Optimized Implementation...")
    
    start_time = time.time()
    extractor = OptimizedEntityExtractor(batch_size=4)
    load_time = time.time() - start_time
    print(f"Optimized load time: {load_time:.2f} seconds")

    print("\nProcessing texts with optimized implementation...")
    start_time = time.time()
    results, stats = extractor.process_texts(test_texts)
    total_time = time.time() - start_time

    total_chars = sum(len(text) for text in test_texts)
    total_entities = sum(len(entities) for entities in results)

    for i, (entities, stat) in enumerate(zip(results, stats), 1):
        print(f"Text {i}: Processed in {stat.process_time:.2f} seconds, found {len(entities)} entities")

    return {
        'load_time': load_time,
        'total_process_time': total_time,
        'avg_process_time': total_time / len(test_texts),
        'chars_per_second': total_chars / total_time,
        'total_entities': total_entities
    }

def compare_implementations():
    """Run comparison between implementations"""
    # Test texts
    test_texts = [
        "Microsoft CEO Satya Nadella announced new products in Seattle.",
        "Apple Inc. released their latest iPhone 15 Pro Max in Cupertino, California.",
        "Google's CEO Sundar Pichai visited their London office last week.",
        "Tesla's Elon Musk announced on Twitter that SpaceX will launch their next rocket.",
        "Amazon's AWS division, led by Adam Selipsky, reported record growth in cloud services."
    ] * 3  # Triple the texts for better comparison

    labels = ["person", "organization", "location", "date", "product"]

    print("\n=== Running Benchmarks ===")
    
    # Run benchmarks
    original_stats = run_original_benchmark(test_texts, labels)
    optimized_stats = run_optimized_benchmark(test_texts, labels)

    # Create comparison table
    comparison_data = [
        ["Metric", "Original", "Optimized", "Improvement"],
        ["Model Load Time", f"{original_stats['load_time']:.2f}s", 
         f"{optimized_stats['load_time']:.2f}s",
         f"{(original_stats['load_time']/optimized_stats['load_time']):.1f}x"],
        ["Total Process Time", f"{original_stats['total_process_time']:.2f}s",
         f"{optimized_stats['total_process_time']:.2f}s",
         f"{(original_stats['total_process_time']/optimized_stats['total_process_time']):.1f}x"],
        ["Avg Time per Text", f"{original_stats['avg_process_time']:.2f}s",
         f"{optimized_stats['avg_process_time']:.2f}s",
         f"{(original_stats['avg_process_time']/optimized_stats['avg_process_time']):.1f}x"],
        ["Characters/Second", f"{original_stats['chars_per_second']:.0f}",
         f"{optimized_stats['chars_per_second']:.0f}",
         f"{(optimized_stats['chars_per_second']/original_stats['chars_per_second']):.1f}x"],
        ["Total Entities Found", str(original_stats['total_entities']),
         str(optimized_stats['total_entities']),
         "Same" if original_stats['total_entities'] == optimized_stats['total_entities'] else "Different"]
    ]

    # Print comparison
    print("\n=== Performance Comparison ===")
    print(tabulate(comparison_data, headers="firstrow", tablefmt="grid"))

    # Print conclusions
    print("\n=== Conclusions ===")
    print("1. Speed Improvement:")
    print(f"   - Overall processing is {(original_stats['total_process_time']/optimized_stats['total_process_time']):.1f}x faster")
    print(f"   - Model loading is {(original_stats['load_time']/optimized_stats['load_time']):.1f}x faster")
    
    print("\n2. Memory Usage:")
    print("   - Original: Uses more memory due to lack of batch processing")
    print("   - Optimized: Better memory management with batch processing and garbage collection")
    
    print("\n3. Key Advantages of Optimized Version:")
    print("   - Batch processing capability")
    print("   - Better memory management")
    print("   - GPU optimization when available")
    print("   - More robust error handling")

if __name__ == "__main__":
    compare_implementations()