import os
import shutil
import yaml

def get_hosting_type():
    """
    Reads the 'config.yaml' file and returns the hosting type that is set to True.
    If no hosting type is set to True, or if multiple hosting types are set to True, an error message is printed.
    """
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    hosting = config["hosting"]
    true_count = 0
    true_key = ""

    for key, value in hosting.items():
        if value == True:
            true_count += 1
            true_key = key

    if true_count == 0:
        print("Erreur : aucun paramètre n'est à True.")
    elif true_count > 1:
        print("Erreur : plusieurs paramètres sont à True.")
    else:
        hosting = true_key

    return hosting


def create_output_dir(hosting_type):
    """
    Creates the output directory path based on the given hosting type.
    """
    if hosting_type == "onpremise":
        return "output/onpremise"
    elif hosting_type == "cloud":
        return "output/cloud"
    else:
        raise ValueError(f"Invalid hosting type: {hosting_type}")


def copy_files(config):
    """
    Copies the necessary files to the output directory based on the given config.
    """
    output_dir = create_output_dir(config["hosting_type"])

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    shutil.copy(f"templates/{config['hosting_type']}/main.tf", output_dir)

    for app, app_config in config.items():
        if app == "hosting_type":
            continue

        if "enable" in app_config and app_config["enable"]:
            shutil.copy(f"templates/{config['hosting_type']}/{app}.tf", output_dir)
            shutil.copy(f"templates/{config['hosting_type']}/{app}.value", output_dir)
            with open(f"{output_dir}/{app}.tf", "r") as f:
                content = f.read()
            content = content.replace("<version>", app_config["version"])
            with open(f"{output_dir}/{app}.tf", "w") as f:
                f.write(content)
            with open(f"{output_dir}/{app}.value", "r") as f:
                content = f.read()
            content = content.replace("<ingresshost>", app_config["ingresshost"])
            with open(f"{output_dir}/{app}.value", "w") as f:
                f.write(content)


def main():
    hosting_type = get_hosting_type()
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    config["hosting_type"] = hosting_type
    copy_files(config)


if __name__ == "__main__":
    main()
