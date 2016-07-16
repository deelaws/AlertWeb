from alert_process_engine import AlertProcessEngine

if __name__ == "__main__":
    engine = AlertProcessEngine()
    engine.configure_engine(10, 10, 1)
    engine.start_engine()

    while("exit" != input("enter exit to quit\n")):
        print("\t Continuing to process records")

    engine.shutdown_engine()
    engine.join_worker_threads()