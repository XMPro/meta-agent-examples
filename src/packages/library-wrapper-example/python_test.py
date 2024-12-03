from MetaPythonRunner import DataProcessor

def main():
    filepath = "another_main.py"
    processor = DataProcessor(filepath, 60)

    create_data = {"foo": "20"}
    on_create_result = processor.execute_on_create(create_data)

    print("on_create result:", on_create_result)

    receive_data = {
        "bar": "10"
    }
    on_receive_result = processor.execute_on_receive(receive_data)

    print("on_receive result:", on_receive_result)

if __name__ == "__main__":
    main()