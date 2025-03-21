# Run test

1. Bật LLM Local
2. Run codegen: 
    cd codegen-agent
    pip install -r requirements.txt
    python main.py
3. Run sast tool
    cd sast-agent
    pip install -r requirements.txt
    python AnalyzeCodeAPI.py
4. Run orchestrator
    cd orchestrator
    pip install -r requirements.txt
    python main.py

# Run itelration repair
python excuteItelration.py
-> chạy test flow itelration. Hiển thị kết quả ở màn console
# Run preshot repair
python excutePreshot.py 
-> chạy test flow preshot repair. Hiển thị kết quả ở màn console
# Run hybrid repair
python excuteHybrid.py 
-> chạy test flow hybrid. Hiển thị kết quả ở màn console
