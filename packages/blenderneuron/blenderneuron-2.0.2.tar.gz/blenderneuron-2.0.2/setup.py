from setuptools import setup, find_packages

with open('README.txt') as file:
    long_description = file.read()

setup(name='blenderneuron',
      version='2.0.2',
      description='Interface for Blender <-> NEURON',
      long_description=long_description,
      author='Justas Birgiolas',
      author_email='justas@asu.edu',
      url='https://BlenderNEURON.org',
      packages=find_packages(),
      platforms=["Linux", "Mac OS", "Windows"],
      keywords=["Blender", "NEURON", "neuroscience", "visualization", "neural networks", "neurons", "3D"],
      license="MIT",
      install_requires=[],
      include_package_data=True,
      package_data={'blenderneuron': ['*.json']},
      classifiers=[
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Operating System :: MacOS",
          "Operating System :: Microsoft :: Windows",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python",
          "Topic :: Scientific/Engineering :: Visualization",
      ]
)
