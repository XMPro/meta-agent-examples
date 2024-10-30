# XMPro Meta Agent Repository

This repository contains a collection of Meta Agents Source Code and configuration intended for use with the XMPro Meta Agent. Each implementation allows designers to innovate quickly by creating agents in languages they are familiar with while leveraging 3rd party libraries.

## Overview

The Meta Action Agent allows designers to innovate quickly, creating agents in languages they are familiar with and leveraging 3rd party libraries.

## Prerequisites

- XMPro Stream Host version 4.4.13 or higher
- Programming language installed on the Stream Host device (Currently supports Python, with more languages planned)
- Required packages either:
  - Referenced in the script (auto-installed)
  - Manually installed on the Stream Host device

## Repository Structure

```
src/
└── packages/
    └── <meta-agent-name>/
        └── action_agent/
            ├── <meta-agent-name>_<meta-agent-version>.xmp
            ├── README.md
            ├── source-code/
            │   ├── <meta-agent-name>.py
            │   └── ...
            └── tests/
                └── <test-name>.py
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/organization/xmpro-meta-agents.git
   ```
2. Navigate to the specific Meta Agent implementation you want to work with:
   ```bash
   cd src/packages/<meta-agent-name>/action_agent
   ```
3. Follow the README.md instructions in the specific Meta Agent's directory for setup and usage.

## Development Guidelines

### Source Code Functions

Each Meta Agent implementation must include these core functions:

1. `on_create(data: dict) -> dict | None`
   - Runs once when the data stream is published
   - Handles static configuration and initialization
   - Returns optional dictionary for debugging

2. `on_receive(data: dict) -> dict`
   - Runs for each event received
   - Processes dynamic values
   - Returns dictionary mapped to Output Endpoint

3. `on_destroy()`
   - Runs when data stream is unpublished
   - Handles resource cleanup

### Best Practices

- Parse string inputs before using as different types
- Use JSON strings for complex data handling
- Implement proper error handling
- Document all inputs and outputs
- Include usage examples
- Write comprehensive tests

## Examples

The repository includes several example implementations:

1. Simple Math Example
   - Demonstrates basic input/output handling
   - Shows configuration of On Create and On Receive functions

2. Library Wrapper Example
   - Shows how to wrap external libraries
   - Demonstrates control loop calculations

## Contributing

To add a new Meta Agent implementation:

1. Create a new branch:
   ```bash
   git checkout -b feature/<meta-agent-name>
   ```
2. Follow the repository structure guidelines
3. Include:
   - Complete source code
   - Comprehensive tests
   - Documentation
   - Usage examples

## Testing

Each Meta Agent implementation should include:
- Unit tests for core functionality
- Integration tests with XMPro Stream Host
- Documentation of test scenarios
- Example configurations

## Support

For support:
- Check the individual Meta Agent's README.md
- Review the implementation examples
- Contact the repository maintainers
- Visit the [XMPro Meta Agent documentation](https://docs.xmpro.com/xmpro-stream-host/meta-agents/introduction/overview/)

## License

MIT License

Copyright (c) 2024 XMPro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.