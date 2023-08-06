"""
This is the core file in the `gradio` package, and defines the Interface class, including methods for constructing the
interface using the input and output types.
"""

import tempfile
import traceback
import webbrowser

import gradio.inputs
import gradio.outputs
from gradio import networking, strings
from distutils.version import StrictVersion
import pkg_resources
import requests
import random
import time
from IPython import get_ipython

LOCALHOST_IP = "127.0.0.1"
TRY_NUM_PORTS = 100
PKG_VERSION_URL = "https://gradio.app/api/pkg-version"


class Interface:
    """
    The Interface class represents a general input/output interface for a machine learning model. During construction,
    the appropriate inputs and outputs
    """

    def __init__(self, fn, inputs, outputs, verbose=False):
        """
        :param fn: a function that will process the input panel data from the interface and return the output panel data.
        :param inputs: a string or `AbstractInput` representing the input interface.
        :param outputs: a string or `AbstractOutput` representing the output interface.
        """
        if isinstance(inputs, str):
            self.input_interface = gradio.inputs.registry[inputs.lower()]()
        elif isinstance(inputs, gradio.inputs.AbstractInput):
            self.input_interface = inputs
        else:
            raise ValueError("Input interface must be of type `str` or `AbstractInput`")
        if isinstance(outputs, str):
            self.output_interface = gradio.outputs.registry[outputs.lower()]()
        elif isinstance(outputs, gradio.outputs.AbstractOutput):
            self.output_interface = outputs
        else:
            raise ValueError(
                "Output interface must be of type `str` or `AbstractOutput`"
            )
        self.predict = fn
        self.verbose = verbose
        self.status = "OFF"
        self.always_flag = False
        self.interactivity_disabled = False
        self.saliency = None


    def update_config_file(self, output_directory):
        networking.set_interface_types_in_config_file(
            output_directory,
            self.input_interface.__class__.__name__.lower(),
            self.output_interface.__class__.__name__.lower(),
        )

        if hasattr(self.input_interface, 'get_sample_inputs'):
            networking.set_sample_data_in_config_file(
                output_directory,
                self.input_interface.get_sample_inputs()
            )

        networking.set_always_flagged_in_config_file(output_directory, self.always_flag)
        networking.set_disabled_in_config_file(output_directory, self.interactivity_disabled)

    def validate(self):
        if self.validate_flag:
            if self.verbose:
                print("Interface already validated")
            return
        validation_inputs = self.input_interface.get_validation_inputs()
        n = len(validation_inputs)
        if n == 0:
            self.validate_flag = True
            if self.verbose:
                print(
                    "No validation samples for this interface... skipping validation."
                )
            return
        for m, msg in enumerate(validation_inputs):
            if self.verbose:
                print(
                    f"Validating samples: {m+1}/{n}  ["
                    + "=" * (m + 1)
                    + "." * (n - m - 1)
                    + "]",
                    end="\r",
                )
            try:
                processed_input = self.input_interface.preprocess(msg)
                prediction = self.predict(processed_input)
            except Exception as e:
                if self.verbose:
                    print("\n----------")
                    print(
                        "Validation failed, likely due to incompatible pre-processing and model input. See below:\n"
                    )
                    print(traceback.format_exc())
                break
            try:
                _ = self.output_interface.postprocess(prediction)
            except Exception as e:
                if self.verbose:
                    print("\n----------")
                    print(
                        "Validation failed, likely due to incompatible model output and post-processing."
                        "See below:\n"
                    )
                    print(traceback.format_exc())
                break
        else:  # This means if a break was not explicitly called
            self.validate_flag = True
            if self.verbose:
                print("\n\nValidation passed successfully!")
            return
        raise RuntimeError("Validation did not pass")

    def launch(self, inline=None, inbrowser=None, share=True, validate=True):
        """
        Standard method shared by interfaces that creates the interface and sets up a websocket to communicate with it.
        :param inline: boolean. If True, then a gradio interface is created inline (e.g. in jupyter or colab notebook)
        :param inbrowser: boolean. If True, then a new browser window opens with the gradio interface.
        :param share: boolean. If True, then a share link is generated using ngrok is displayed to the user.
        :param validate: boolean. If True, then the validation is run if the interface has not already been validated.
        """
        # if validate and not self.validate_flag:
        #     self.validate()

        # If an existing interface is running with this instance, close it.
        if self.status == "RUNNING":
            if self.verbose:
                print("Closing existing server...")
            if self.simple_server is not None:
                try:
                    networking.close_server(self.simple_server)
                except OSError:
                    pass

        output_directory = tempfile.mkdtemp()
        # Set up a port to serve the directory containing the static files with interface.
        server_port, httpd = networking.start_simple_server(self, output_directory)
        path_to_local_server = "http://localhost:{}/".format(server_port)
        networking.build_template(
            output_directory, self.input_interface, self.output_interface
        )

        self.update_config_file(output_directory)

        self.status = "RUNNING"
        self.simple_server = httpd

        is_colab = False
        try:  # Check if running interactively using ipython.
            from_ipynb = get_ipython()
            if "google.colab" in str(from_ipynb):
                is_colab = True
        except NameError:
            pass

        try:
            current_pkg_version = pkg_resources.require("gradio")[0].version
            latest_pkg_version = requests.get(url=PKG_VERSION_URL).json()["version"]
            if StrictVersion(latest_pkg_version) > StrictVersion(current_pkg_version):
                print(f"IMPORTANT: You are using gradio version {current_pkg_version}, "
                      f"however version {latest_pkg_version} "
                      f"is available, please upgrade.")
                print('--------')
        except:  # TODO(abidlabs): don't catch all exceptions
            pass

        if self.verbose:
            print(strings.en["BETA_MESSAGE"])
            if not is_colab:
                print(strings.en["RUNNING_LOCALLY"].format(path_to_local_server))
        if share:
            try:
                share_url = networking.setup_tunnel(server_port)
            except RuntimeError:
                share_url = None
                if self.verbose:
                    print(strings.en["NGROK_NO_INTERNET"])
        else:
            if (
                is_colab
            ):  # For a colab notebook, create a public link even if share is False.
                share_url = networking.setup_tunnel(server_port)
                if self.verbose:
                    print(strings.en["COLAB_NO_LOCAL"])
            else:  # If it's not a colab notebook and share=False, print a message telling them about the share option.
                if self.verbose:
                    print(strings.en["PUBLIC_SHARE_TRUE"])
                share_url = None

        if share_url is not None:
            networking.set_share_url_in_config_file(output_directory, share_url)
            if self.verbose:
                print(strings.en["GENERATING_PUBLIC_LINK"], end='\r')
                time.sleep(5)
                print(strings.en["MODEL_PUBLICLY_AVAILABLE_URL"].format(share_url))

        if inline is None:
            try:  # Check if running interactively using ipython.
                get_ipython()
                inline = True
                if inbrowser is None:
                    inbrowser = False
            except NameError:
                inline = False
                if inbrowser is None:
                    inbrowser = True
        else:
            if inbrowser is None:
                inbrowser = False

        if inbrowser and not is_colab:
            webbrowser.open(
                path_to_local_server
            )  # Open a browser tab with the interface.
        if inline:
            from IPython.display import IFrame, display

            if (
                is_colab
            ):  # Embed the remote interface page if on google colab; otherwise, embed the local page.
                display(IFrame(share_url, width=1000, height=500))
            else:
                display(IFrame(path_to_local_server, width=1000, height=500))

        return httpd, path_to_local_server, share_url
