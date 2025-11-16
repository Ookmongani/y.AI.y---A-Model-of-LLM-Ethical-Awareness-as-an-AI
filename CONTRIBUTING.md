# Contributing to y.AI.y

Thank you for your interest in contributing to y.AI.y! This project is focused on ethical awareness in LLMs with security and reproducibility as core principles.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Prioritize security and ethical considerations
- Maintain reproducibility in all changes

## Getting Started

1. Fork the repository
2. Clone your fork
3. Install dependencies: `./scripts/install.sh`
4. Run tests: `pytest yaiy/tests/`

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow existing code style
- Add tests for new features
- Update documentation as needed
- Maintain security-first approach

### 3. Test Your Changes

```bash
# Run all tests
pytest yaiy/tests/ -v

# Run with coverage
pytest yaiy/tests/ --cov=yaiy

# Test specific components
python -m yaiy.signer.cli generate
python -m yaiy.simulation.ucf_sim --iterations 5
```

### 4. Commit

```bash
git add .
git commit -m "Brief description of changes"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Security Guidelines

**CRITICAL:** Never commit:
- Private keys
- Secrets or credentials
- Unverified model weights
- Personal data

**ALWAYS:**
- Use offline-first design patterns
- Require manual approval for sensitive operations
- Include cryptographic verification
- Maintain reproducibility

## Testing Requirements

All contributions must include:

- Unit tests for new features
- Tests must pass locally before PR
- Coverage should not decrease
- Tests should be reproducible

Example test structure:

```python
def test_new_feature():
    """Test description."""
    # Arrange
    input_data = {...}
    
    # Act
    result = new_feature(input_data)
    
    # Assert
    assert result is not None
    assert result.property == expected_value
```

## Documentation

Update documentation when:

- Adding new features
- Changing existing behavior
- Adding new dependencies
- Modifying security policies

Documentation includes:
- Docstrings in code
- README updates
- Example updates
- SECURITY.md if security-related

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write clear, descriptive docstrings
- Keep functions focused and small
- Add comments for complex logic

Example:

```python
def process_data(data: Dict[str, Any], verify: bool = True) -> ProcessedData:
    """
    Process and verify input data.
    
    Args:
        data: Input data dictionary
        verify: Whether to verify cryptographic signatures
        
    Returns:
        ProcessedData object with verified data
        
    Raises:
        ValueError: If data format is invalid
        SignatureError: If signature verification fails
    """
    # Implementation
```

## Pull Request Checklist

Before submitting a PR:

- [ ] Tests pass locally
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] Security considerations addressed
- [ ] No private keys or secrets committed
- [ ] Reproducibility maintained
- [ ] CI checks pass

## Areas for Contribution

### High Priority
- Additional policy rules
- More comprehensive tests
- Documentation improvements
- Security enhancements
- Performance optimizations

### Medium Priority
- Additional simulation metrics
- Visualization improvements
- CLI enhancements
- Error handling improvements

### Low Priority
- Code refactoring
- Minor bug fixes
- Typo corrections

## Questions?

- Open an issue for discussion
- Check existing issues and PRs
- Review documentation first

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
