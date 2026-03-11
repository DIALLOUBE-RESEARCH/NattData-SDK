from setuptools import setup, find_packages

setup(
    name="nattdata",
    version="1.1.0",
    description="NattSwap SDK — Cross-chain swaps with NDAT rewards for AI agents",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="HyperNatt",
    author_email="contact@hypernatt.com",
    url="https://github.com/DIALLOUBE-RESEARCH/NATTAPP-portfolio",
    project_urls={
        "Homepage": "https://hypernatt.com",
        "MCP Tools": "https://hypernatt.com/mcp/tools",
        "BaseScan NDAT": "https://basescan.org/token/0x7601550Ce343B8EC89ecC973987d68b938Bd77dd",
    },
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="nattswap ndat ai-agent cross-chain swap defi base ethereum",
)
