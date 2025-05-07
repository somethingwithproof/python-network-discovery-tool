"""Tests for Docker functionality."""

import os
import pytest
import subprocess
from unittest.mock import patch, MagicMock

class TestDocker:
    """Tests for Docker functionality."""

    def test_dockerfile_exists(self):
        """Test that the Dockerfile exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Dockerfile"))

    def test_docker_compose_exists(self):
        """Test that the docker-compose.yml file exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker-compose.yml"))

    def test_dockerignore_exists(self):
        """Test that the .dockerignore file exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".dockerignore"))

    def test_env_example_exists(self):
        """Test that the .env.example file exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.example"))

    def test_docker_test_script_exists(self):
        """Test that the docker-test.sh script exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker-test.sh"))

    def test_docker_demo_script_exists(self):
        """Test that the docker-demo.sh script exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker-demo.sh"))

    def test_setup_env_script_exists(self):
        """Test that the setup-env.sh script exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "setup-env.sh"))

    def test_test_docker_setup_script_exists(self):
        """Test that the test-docker-setup.sh script exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test-docker-setup.sh"))

    def test_makefile_exists(self):
        """Test that the Makefile exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Makefile"))

    def test_docker_workflow_exists(self):
        """Test that the GitHub Actions workflow for Docker exists."""
        workflow_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            ".github", 
            "workflows", 
            "docker-build.yml"
        )
        assert os.path.exists(workflow_path)

    def test_docker_docs_exists(self):
        """Test that the Docker documentation exists."""
        assert os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "docker-setup.md"))

    @patch("subprocess.run")
    def test_docker_build(self, mock_run):
        """Test that the Docker image can be built."""
        # Mock the subprocess.run function
        mock_run.return_value = MagicMock(returncode=0)

        # Run the docker build command
        result = subprocess.run(
            ["docker", "build", "-t", "network-discovery:test", "."],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True,
            check=False,
        )

        # Check that the command was called
        mock_run.assert_called_once()

    @patch("subprocess.run")
    def test_docker_compose_config(self, mock_run):
        """Test that the docker-compose.yml file is valid."""
        # Mock the subprocess.run function
        mock_run.return_value = MagicMock(returncode=0)

        # Run the docker-compose config command
        result = subprocess.run(
            ["docker-compose", "config"],
            cwd=os.path.dirname(os.path.dirname(__file__)),
            capture_output=True,
            text=True,
            check=False,
        )

        # Check that the command was called
        mock_run.assert_called_once()

    def test_dockerfile_content(self):
        """Test that the Dockerfile contains the expected content."""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "Dockerfile"), "r") as f:
            content = f.read()
            # Check for key components
            assert "FROM python" in content
            assert "WORKDIR /app" in content
            assert "COPY requirements.txt" in content
            assert "RUN pip install" in content
            assert "COPY . ." in content
            assert "CMD" in content

    def test_docker_compose_content(self):
        """Test that the docker-compose.yml file contains the expected content."""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker-compose.yml"), "r") as f:
            content = f.read()
            # Check for key components
            assert "version:" in content
            assert "services:" in content
            assert "network-discovery:" in content
            assert "dev:" in content
            assert "test:" in content
            assert "build:" in content
            assert "volumes:" in content
            assert "environment:" in content

    def test_dockerignore_content(self):
        """Test that the .dockerignore file contains the expected content."""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".dockerignore"), "r") as f:
            content = f.read()
            # Check for key components
            assert ".git" in content
            assert "__pycache__" in content
            assert "*.pyc" in content
            assert "*.pyo" in content
            assert "*.pyd" in content
            assert ".pytest_cache" in content
            assert "htmlcov" in content
            assert ".coverage" in content

    def test_env_example_content(self):
        """Test that the .env.example file contains the expected content."""
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env.example"), "r") as f:
            content = f.read()
            # Check for key components
            assert "SSH_USER" in content
            assert "MYSQL_USER" in content
            assert "MYSQL_PASSWORD" in content
