from stock_predictor import StockPredictor
import numpy as np

def main(ticker):
    # Use AAPL as default ticker for testing
    ticker = ticker
    print(f"Using ticker: {ticker}")
    
    predictor = StockPredictor(ticker)
    predictions, actual_values = predictor.train()
    
    if predictor.get_best_params():
        print("\nBest hyperparameters found:")
        for param, value in predictor.get_best_params().items():
            print(f"{param}: {value}")
    
    print("\nPrediction Results:")
    print("Last 20 predictions vs actual values:")
    for pred, actual in zip(predictions[-20:], actual_values[-20:]):
        predicted_value = float(pred[0])
        actual_value = float(actual)
        print(
            f"Predicted: ${predicted_value:.2f} | "
            f"Actual: ${actual_value:.2f} | "
            f"Diff: ${abs(predicted_value - actual_value):.2f}"
        )
    
    # Calculate error metrics
    predictions = predictions.reshape(-1)
    actual_values = actual_values.reshape(-1)
    
    # Remove any potential NaN or infinite values
    mask = ~np.isnan(predictions) & ~np.isinf(predictions) & ~np.isnan(actual_values) & ~np.isinf(actual_values)
    predictions = predictions[mask]
    actual_values = actual_values[mask]
    
    mse = np.mean((predictions - actual_values) ** 2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((actual_values - predictions) / actual_values)) * 100
    
    print("\nError Metrics:")
    print(f"Root Mean Square Error: ${rmse:.2f}")
    print(f"Mean Absolute Percentage Error: {mape:.2f}%")

if __name__ == "__main__":
    for ticker in ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "META", "NFLX", "NVDA", "AMC", "DIS"]:
        main(ticker)
