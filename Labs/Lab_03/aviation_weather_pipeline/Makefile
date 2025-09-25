.PHONY: all fetch analyze clean

analyze: fetch
	@echo "Starting analysis of METAR data..."
	./analyze_data.sh
	@echo "Analysis complete. Weather report generated at weather_report.csv"
	@echo "Pipeline completed successfully!"

fetch:
	@echo "Starting METAR data fetch..."
	./fetch_metars.sh
	@echo "METAR data fetch complete. Raw data stored in raw_metars/ directory"
	
clean:
	echo "Starting cleanup.."
	rm -rf raw_metars/ weather_report.csv
	@echo "Cleanup complete!"

all: analyze
