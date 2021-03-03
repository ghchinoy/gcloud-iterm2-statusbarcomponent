#!/usr/bin/env python3
import iterm2
import shlex
import subprocess
from pathlib import Path
import asyncio

gcloud_project = str(Path.home()) + '/dev/google-cloud-sdk/bin/gcloud config get-value project'

def getGcloudProject():
    gcloud_project = str(Path.home()) + '/dev/google-cloud-sdk/bin/gcloud config get-value project'
    proc =  subprocess.Popen(
            shlex.split(gcloud_project),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    stdout, stderr = proc.communicate()
    return f'☁ {stdout.decode().strip()}' if not stderr else '☁ gcloud not installed!'

def listGcloudProjects():
    gcloud_projects = str(Path.home()) + '/dev/google-cloud-sdk/bin/gcloud projects list'
    proc =  subprocess.Popen(
            shlex.split(gcloud_projects),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    stdout, stderr = proc.communicate()
    projectlistall = f'{stdout.decode()}'.split()
    
    projectlist = projectlistall[3:]
    print(projectlist)
    return ''.join(map(str, projectlist))

async def main(connection):
    # Define the configuration knobs:
    knobs = []
    component = iterm2.StatusBarComponent(
        short_description="gcloud Project",
        detailed_description="Google Cloud Project Name",
        knobs=knobs,
        exemplar=getGcloudProject(),
        update_cadence=10,
        identifier="com.chinoy.iterm2-components.gcloud-project")

    @iterm2.StatusBarRPC
    async def coro(
            knobs,
            project=iterm2.Reference("iterm2.user.gcloudproject?")):
        return getGcloudProject()

    @iterm2.RPC
    async def click_handler(project):
        await component.async_open_popover(
            project,
            listGcloudProjects(),
            iterm2.Size(200,200))
  
    # Register the component.
    await component.async_register(connection, coro, onclick = click_handler)

iterm2.run_forever(main)
