#!/usr/bin/env python3
import iterm2
import shlex
import subprocess
from pathlib import Path

def getGcloudProject():
    home = str(Path.home())
    gcloud_project = home + '/dev/google-cloud-sdk/bin/gcloud config get-value project'
    projectbytes = subprocess.check_output(shlex.split(gcloud_project))
    project = projectbytes.decode().rstrip()
    #print(project)
    return "{}".format(project)

async def main(connection):
    # Define the configuration knobs:
    knobs = []
    component = iterm2.StatusBarComponent(
        short_description="gcloud Project",
        detailed_description="Google Cloud Project Name",
        knobs=knobs,
        exemplar=getGcloudProject(),
        update_cadence=10,
        identifier="com.github.ghchinoy.gcloud-project")

    # This function gets called whenever any of the paths named in defaults (below) changes
    # or its configuration changes.
    # References specify paths to external variables (like rows) and binds them to
    # arguments to the registered function (coro). When any of those variables' values
    # change the function gets called.
    @iterm2.StatusBarRPC
    async def coro(
            knobs,
            project=iterm2.Reference("iterm2.user.gcloudproject?")):
        return getGcloudProject()
  
    # Register the component.
    await component.async_register(connection, coro)

iterm2.run_forever(main)
