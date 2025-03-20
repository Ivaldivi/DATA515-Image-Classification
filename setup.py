from setuptools import setup, find_packages

setup(
    name="walandmarks",
    version="0.1",
    packages=['walandmarks'],
    include_package_data = True,
    package_data = {"walandmarks": ["data/*.csv", "images/*", "model/*.png", "walandmarks\model\final_EfficientNetb0_WA_landmarks_model.keras", "model/*.md"],},
    install_requires=[]
)
