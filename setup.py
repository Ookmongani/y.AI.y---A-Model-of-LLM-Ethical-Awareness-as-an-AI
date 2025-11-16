from setuptools import setup, find_packages

with open("README_YAIY.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yaiy",
    version="0.1.0",
    author="y.AI.y Contributors",
    description="Secure Local-First LLM Ethical Awareness Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ookmongani/y.AI.y---A-Model-of-LLM-Ethical-Awareness-as-an-AI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "cryptography>=41.0.7",
        "pynacl>=1.5.0",
        "matplotlib>=3.8.2",
        "numpy>=1.26.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
            "flake8>=6.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "yaiy-signer=yaiy.signer.cli:main",
            "yaiy-simulate=yaiy.simulation.ucf_sim:main",
            "yaiy-plot=yaiy.plotting.tools:main",
        ],
    },
)
