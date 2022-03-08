import argparse
from pipeline import PipelineExecutor
from default_plugins.Header.header import Header
from default_plugins.Params.params import Params
from plugins.custom import CustomPlugin

def main():
    parser = argparse.ArgumentParser("Command parser")
    pipeline = PipelineExecutor(parser)

    default_plugins = [Header(), Params(), CustomPlugin()]
    print(pipeline.execute_pipeline(default_plugins, "input", "xml"))


if __name__ == '__main__':
    main()