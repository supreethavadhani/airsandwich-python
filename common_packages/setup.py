from setuptools import setup, find_packages

setup(
    name="error_lib",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["Flask"],
    description="Common error handling library for microservices",
    author="Your Name",
    author_email="your.email@example.com",  # Optional: Add GitHub URL
)
