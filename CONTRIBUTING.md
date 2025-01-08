# Contributing to XMPro Meta Agent Repository

This guide will help you contribute new Meta Agents to this repository. We follow a standard structure and set of best practices to ensure consistency and quality across all Meta Agents.

## Table of Contents
- [Getting Started](#getting-started)
- [Meta Agent Structure](#meta-agent-structure)
- [Development Guidelines](#development-guidelines)
- [Testing Requirements](#testing-requirements)
- [Documentation Requirements](#documentation-requirements)
- [Pull Request Process](#pull-request-process)

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/organization/xmpro-meta-agents.git
   ```
2. Create a new branch for your Meta Agent:
   ```bash
   git checkout -b feature/your-meta-agent-name
   ```

## Meta Agent Structure

Your Meta Agent must follow this directory structure:

```
src/packages/<meta-agent-name>/action_agent/
├── <meta-agent-name>_<meta-agent-version>.xmp
├── README.md
└── source-code/
    ├── <meta-agent-name>.py
    └── ...
└── tests/
    └── <test-name>.py
```

### Required Files

#### 1. Meta Agent Package File (`<meta-agent-name>_<meta-agent-version>.xmp`)
- Contains the Meta Agent configuration
- Includes input/output mappings
- Version number must follow semantic versioning

#### 2. Python Source File (`<meta-agent-name>.py`)
- Must implement the required functions:
  - `on_create(data: dict) -> dict | None`
  - `on_receive(data: dict) -> dict`
  - `on_destroy()`
- Include error handling
- Example structure:
  ```python
  def on_create(data: dict) -> dict | None:
      try:
          # Initialize your variables/services
          return {"status": "initialized"}
      except Exception as e:
          print(f"Error in on_create: {str(e)}")
          return None

  def on_receive(data: dict) -> dict:
      try:
          # Process incoming data
          return {"processed_value": result}
      except Exception as e:
          print(f"Error in on_receive: {str(e)}")
          return {}

  def on_destroy():
      # Clean up resources
      pass
  ```

#### 3. README.md
- Provides detailed documentation
- Includes usage examples
- Documents configuration parameters
- Explains the purpose and functionality

## Development Guidelines

### 1. Input/Output Configuration
- Define clear input mappings
- Document all output parameters
- Example:
  ```python
  # Input configuration
  {
      "initial_value": "100",
      "threshold": "0.5"
  }

  # Output mapping
  {
      "result": "Double",
      "status": "String"
  }
  ```

### 2. Error Handling
- Implement comprehensive error handling
- Log meaningful error messages
- Handle all potential exceptions
- Return appropriate error states

### 3. Package Management
- List all required packages in README
- Use standard Python packages when possible
- Document any special installation requirements

### 4. State Management
- Handle initialization properly in `on_create`
- Clean up resources in `on_destroy`
- Maintain state efficiently between events

## Testing Requirements

### 1. Unit Tests
- Write tests for all major functions
- Include edge cases and error conditions
- Test input/output mappings
- Maintain test coverage above 80%

### 2. Integration Tests
- Test with actual XMPro Stream Host
- Verify performance with large datasets
- Test error handling scenarios

## Documentation Requirements

### 1. README.md
Your Meta Agent must include a README.md with:
- Clear description of functionality
- Installation instructions
- Configuration parameters
- Usage examples with sample data
- Performance considerations
- Troubleshooting guide

### 2. Code Documentation
- Add docstrings for all functions
- Document parameters and return values
- Explain complex logic
- Include usage examples in comments

## Pull Request Process

1. Create a new branch for your Meta Agent
2. Implement your Meta Agent following the guidelines
3. Test thoroughly
4. Update documentation
5. Submit a pull request with:
   - Description of the Meta Agent
   - Test results
   - Performance metrics
   - Any special considerations

### Pull Request Checklist

- [ ] Follows directory structure
- [ ] Includes complete README.md
- [ ] Implements required functions
- [ ] Includes unit tests
- [ ] Code is documented
- [ ] Tests pass
- [ ] Performance tested
- [ ] Documentation complete

## Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your Meta Agent will be merged

## Need Help?

- Check existing Meta Agents for examples
- Review the Simple Math Example and Library Wrapper Example
- Create an issue for questions
- Refer to the Meta Agent documentation

## Best Practices

### Code Quality
- Follow PEP 8 style guide
- Use type hints
- Keep functions focused and small
- Comment complex algorithms

### Performance
- Optimize for large data sets
- Minimize memory usage
- Handle resources efficiently
- Test with realistic data volumes

### Security
- Validate all inputs
- Handle sensitive data appropriately
- Follow security best practices
- Document security considerations

## Code of Conduct

- Be respectful and professional
- Follow established patterns
- Help others succeed
- Maintain code quality standards

Thank you for contributing to the XMPro Meta Agent repository!