from setuptools import setup

setup(
    name="isityaml",
    version="0.8",
    description="A Django app (with tags) for checking the correctness of YAML",
    author="Peter Murphy",
    author_email="peterkmurphy@gmail.com",
    url="https://pypi.org/project/isityaml/",
    packages=["isityaml", "isityaml.templatetags"],
    package_data={
        "isityaml": [
            "templates/isityaml/*.html",
            "static/isityaml/*.css",
        ],
    },
    keywords="YAML parse text Django",
    license="BSD-3-Clause",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.2",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Education",
    ],
    long_description=open("README.md").read(),  # noqa: SIM115
    long_description_content_type="text/markdown",
    install_requires=["Django >= 5.2", "PyYAML >= 6.0"],
)
