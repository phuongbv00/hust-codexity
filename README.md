# Run test

1. Bật LLM Local
2. Run codegen: 
    cd codegen-agent
    python main.py
3. Run sast tool
    cd sast-agent
    python AnalyzeCodeAPI.py
4. Run orchestrator
    cd orchestrator
    python main.py

Click excuteItelration.exe -> chạy test flow itelration. Có kết quả ở màn console
Click excutePreshot.exe -> chạy test flow preshot repair. Có kết quả ở màn console
