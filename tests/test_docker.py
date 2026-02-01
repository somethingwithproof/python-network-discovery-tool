"""Tests for Docker functionality."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch


# Project root is one directory above the tests directory
PROJECT_ROOT = Path(__file__).parent.parent


class TestDocker:
    """Tests for Docker functionality."""

    def test_dockerfile_exists(self):
        """Test that the Dockerfile exists."""
        assert (PROJECT_ROOT / "Dockerfile").exists()

    def test_docker_compose_exists(self):
        """Test that the docker-compose.yml file exists."""
        assert (PROJECT_ROOT / "docker-compose.yml").exists()

    def test_dockerignore_exists(self):
        """Test that the .dockerignore file exists."""
        assert (PROJECT_ROOT / ".dockerignore").exists()

    def test_env_example_exists(self):
        """Test that the .env.example file exists."""
        assert (PROJECT_ROOT / ".env.example").exists()

    def test_docker_test_script_exists(self):
        """Test that the docker-test.sh script exists."""
        assert (PROJECT_ROOT / "docker-test.sh").exists()

    def test_docker_demo_script_exists(self):
        """Test that the docker-demo.sh script exists."""
        assert (PROJECT_ROOT / "docker-demo.sh").exists()

    def test_setup_env_script_exists(self):
        """Test that the setup-env.sh script exists."""
        assert (PROJECT_ROOT / "setup-env.sh").exists()

    def test_test_docker_setup_script_exists(self):
        """Test that the test-docker-setup.sh script exists."""
        assert (PROJECT_ROOT / "test-docker-setup.sh").exists()

    def test_makefile_exists(self):
        """Test that the Makefile exists."""
        assert (PROJECT_ROOT / "Makefile").exists()

    def test_docker_workflow_exists(self):
        """Test that the GitHub Actions workflow for Docker exists."""
        workflow_path = PROJECT_ROOT / ".github" / "workflows" / "docker-build.yml"
        assert workflow_path.exists()

    def test_docker_docs_exists(self):
        """Test that the Docker documentation exists."""
        assert (PROJECT_ROOT / "docs" / "docker-setup.md").exists()

    @patch("subprocess.run")
    def test_docker_build(self, mock_run):
        """Test that the Docker image can be built."""
        mock_run.return_value = MagicMock(returncode=0)

        subprocess.run(
            ["docker", "build", "-t", "network-discovery:test", "."],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )

        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_docker_compose_config(self, mock_run):
        """Test that the docker-compose.yml file is valid."""
        mock_run.return_value = MagicMock(returncode=0)

        subprocess.run(
            ["docker-compose", "config"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )

        mock_run.assert_called_once()

    def test_dockerfile_content(self):
        """Test that the Dockerfile contains the expected content."""
        content = (PROJECT_ROOT / "Dockerfile").read_text()
        assert "FROM python" in content
        assert "WORKDIR /app" in content
        assert "COPY pyproject.toml" in content
        assert "uv" in content
        assert "CMD" in content

    def test_docker_compose_content(self):
        """Test that the docker-compose.yml file contains the expected content."""
        content = (PROJECT_ROOT / "docker-compose.yml").read_text()
        assert "services:" in content
        assert "network-discovery:" in content
        assert "dev:" in content
        assert "test:" in content
        assert "build:" in content
        assert "volumes:" in content
        assert "environment:" in content

    def test_dockerignore_content(self):
        """Test that the .dockerignore file contains the expected content."""
        content = (PROJECT_ROOT / ".dockerignore").read_text()
        assert ".git" in content
        assert "__pycache__" in content
        assert "*.py[cod]" in content or "*.pyc" in content
        assert ".pytest_cache" in content
        assert "htmlcov" in content
        assert ".coverage" in content

    def test_env_example_content(self):
        """Test that the .env.example file contains the expected content."""
        content = (PROJECT_ROOT / ".env.example").read_text()
        assert "SSH_USER" in content
        assert "MYSQL_USER" in content
        assert "MYSQL_PASSWORD" in content
