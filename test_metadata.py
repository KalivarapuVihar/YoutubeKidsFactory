from utils.run_manager import RunManager


def main():

    run = RunManager("Test Metadata")

    run.initialize()

    run.create_metadata()

    run.update_metadata(
        status="storyboard_completed",
        scenes=10,
    )

    print(
        f"Metadata created at:\n"
        f"{run.metadata_path}"
    )


if __name__ == "__main__":
    main()