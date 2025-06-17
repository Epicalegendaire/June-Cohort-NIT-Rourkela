import shutil
import site
import os

def install_package(src_path, package_name):
    site_packages = site.getsitepackages()[0]
    dest_path = os.path.join(site_packages, package_name)

    if os.path.exists(dest_path):
        print(f"Removing old version at {dest_path}")
        shutil.rmtree(dest_path)

    print(f"Copying {package_name} to {dest_path}")
    shutil.copytree(src_path, dest_path)
    print("Installation complete.")

# Example usage
if __name__ == "__main__":
    install_package("admin_black", "admin_black")
