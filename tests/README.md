# Tests

Test suite for self-improving-factory.

## Structure

```
tests/
├── conftest.py                 # Pytest fixtures
├── unit/                       # Unit tests (fast, isolated)
└── integration/                # Integration tests (may invoke external processes)
    └── test_provisioning_smoke.py  # Quickflow agent smoke tests
```

## Running Tests

### Prerequisites

1. Install test dependencies:
   ```bash
   pip install -r requirements.txt
   # or
   pip install -e ".[dev]"
   ```

2. For integration tests, ensure Claude CLI is installed:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

3. Ensure test project directory exists:
   ```bash
   mkdir -p ~/repos/test-project
   ```

### Run All Unit Tests

```bash
pytest tests/unit/
```

### Run Integration Tests

Integration tests are marked and skipped by default. To run them:

```bash
# Run all integration tests
pytest tests/integration/ -m integration

# Run the Quickflow smoke test specifically
pytest tests/integration/test_provisioning_smoke.py -v
```

### Run Structure Tests Only (Fast)

These tests verify provisioning structure without invoking Claude CLI:

```bash
pytest tests/integration/test_provisioning_smoke.py::TestProvisioningStructure -v
```

### Run Full Smoke Test (Slow)

This invokes Claude CLI and may take 1-2 minutes:

```bash
pytest tests/integration/test_provisioning_smoke.py::TestProvisioningSmokeTest -v --timeout=300
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `@pytest.mark.integration` | Integration test (may invoke external processes) |
| `@pytest.mark.slow` | Slow running test |
| `@pytest.mark.requires_claude` | Requires Claude CLI to be installed |

## Test Project

Integration tests use `~/repos/test-project` as the target directory.

### Teardown Protocol

Per project requirements:
- Delete everything locally **except** the project folder
- Preserves folder structure for rapid dev/test cycles
- Git directory optionally preserved

## Coverage

Run with coverage:

```bash
pytest --cov=db --cov-report=html tests/
```

## Smoke Test Details

### test_quickflow_implements_python_hello_world

This test:
1. Provisions a test project with CLAUDE.md and BMAD
2. Invokes Claude CLI with a prompt for the Quickflow agent
3. Agent implements Python hello world with TDD
4. Verifies hello.py exists and runs correctly

### test_quickflow_with_slash_command

This test:
1. Provisions a test project
2. Invokes Claude CLI with agent activation prompt
3. Agent creates a utility function
4. Verifies the function was created
