#!/usr/bin/env python3

from aws_cdk import core

from new.new_stack import NewStack


app = core.App()
NewStack(app, "new")

app.synth()
