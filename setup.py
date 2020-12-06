from setuptools import setup, find_packages

setup(
    name="fortress-analyzer",
    description="Fortress is a Solidity static analysis framework written in Python 3.",
    url="https://github.com/fortressfoundation/fortress-security-audit-engine",
    author="Fortress",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "prettytable>=0.7.2",
        "pysha3>=1.0.2",
        # "crytic-compile>=0.1.10",
        "crytic-compile",
    ],
    dependency_links=["git+https://github.com/crytic/crytic-compile.git@master#egg=crytic-compile"],
    license="AGPL-3.0",
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": [
            "fortress = fortress.__main__:main",
            "fortress-check-upgradeability = fortress.tools.upgradeability.__main__:main",
            "fortress-find-paths = fortress.tools.possible_paths.__main__:main",
            "fortress-simil = fortress.tools.similarity.__main__:main",
            "fortress-flat = fortress.tools.flattening.__main__:main",
            "fortress-format = fortress.tools.fortress_format.__main__:main",
            "fortress-check-erc = fortress.tools.erc_conformance.__main__:main",
            "fortress-check-kspec = fortress.tools.kspec_coverage.__main__:main",
            "fortress-prop = fortress.tools.properties.__main__:main",
            "fortress-mutate = fortress.tools.mutator.__main__:main",
        ]
    },
)
