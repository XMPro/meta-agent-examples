# Simple Math Example

The `simple-math-example` folder contains two main files to be used by the Meta Action Agent. 
- `calculations/main.py`
- `another_main.py`

This is a demo on how to use a repository as the Meta Agent Source Code

## Features
Does simple arithmetic calculations from a static value `foo` and a dyanmic `bar` value.
- Addition
- Subtraction
- Multiplication

## Usage

To use the functions on the Data Stream. Configure the Meta Action Agent:
- Use this Git Repository and set on of the main files as the Main Source Code Path.
- Assign a value `foo` on the On Create configuration
- Assign a value `bar` on the On Receive configuration
- Configure Output Paylod: `foobar`, `sum`, `diff`, and `product`


## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
