import click
import tpudiepie
import json
import sys
import os
import time
from pprint import pprint as pp

import logging as pylogging
logging = tpudiepie.logger
logging.setLevel(pylogging.WARNING)

@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.pass_context
def cli(ctx, **kws):
  ctx.obj = kws
  verbose = ctx.obj['verbose']
  if verbose:
    logging.setLevel(pylogging.DEBUG)
  logging.debug('%r', sys.argv)

def print_tpu_status_headers(color=True):
  message = tpudiepie.format(tpudiepie.format_headers())
  if color:
    click.secho(message, bold=color)
  else:
    click.echo(message)

def print_tpu_status(tpu, color=True):
  message = tpudiepie.format(tpu)
  if not color:
    click.echo(message)
  else:
    status = tpudiepie.format(tpu, '{status}')
    health = tpudiepie.format(tpu, '{health}')
    if status == 'READY' and health == 'HEALTHY':
      click.secho(message, fg='green')
      return 'HEALTHY'
    elif status == 'PREEMPTED':
      click.secho(message, fg='red')
    else:
      click.secho(message, fg='yellow')

def print_tpus_status(zone=None, format='text', color=True):
  tpus = tpudiepie.get_tpus(zone=zone)
  if format == 'json':
    click.echo(json.dumps(tpus))
  else:
    assert format == 'text'
    print_tpu_status_headers(color=color)
    for tpu in tpus:
      print_tpu_status(tpu, color=color)

def watch_status():
  while True:
    click.clear()
    print_tpus_status()
    time.sleep(5.0)

@cli.command()
def top():
  watch_status()

@cli.command()
def tail():
  watch_status()

@cli.command("list")
@click.option('--zone', type=click.Choice(tpudiepie.tpu.get_tpu_zones()))
@click.option('--format', type=click.Choice(['text', 'json']), default='text')
@click.option('-c/-nc', '--color/--no-color', default=True)
def list_tpus(zone, format, color):
  print_tpus_status(zone=zone, format=format, color=color)

def complete_tpu_id(ctx, args, incomplete, zone=None):
  tpus = tpudiepie.get_tpus(zone=zone)
  return [tpudiepie.tpu.parse_tpu_id(tpu) for tpu in tpus]

# @cli.command()
# @click.argument('tpu', type=click.STRING, autocompletion=complete_tpu_id)
# @click.option('--zone', type=click.Choice(tpudiepie.tpu.get_tpu_zones()))
# def create(tpu, zone):
#   tpu = tpudiepie.get_tpu(tpu=tpu, zone=zone)
#   create = tpudiepie.create_tpu_command(tpu)
#   click.echo(create)

def check_healthy(tpu, zone=None, color=True):
  tpu = tpudiepie.get_tpu(tpu, zone=zone)
  print_tpu_status(tpu, color=color)
  status = tpudiepie.format(tpu, '{status}')
  health = tpudiepie.format(tpu, '{health}')
  if status == 'READY' and health == 'HEALTHY':
    return True
  return False

def wait_healthy(tpu, zone=None, color=True):
  while True:
    if check_healthy(tpu, color=color):
      return
    click.echo('TPU {} not yet healthy; waiting 30 seconds...'.format(tpudiepie.tpu.parse_tpu_id(tpu)))
    time.sleep(30.0)

def print_step(label=None, command=None):
  click.echo('')
  if label is not None:
    click.secho(label, bold=True)
  if command is not None and not callable(command):
    click.echo('  $ ', nl=False)
    click.secho(command, fg='blue', bold=True)

def do_step(label=None, command=None, dry_run=False, delay_after=1.0):
  print_step(label=label, command=command)
  if command is not None:
    if dry_run:
      click.echo('Dry run; command skipped.')
      time.sleep(3.0)
    else:
      if callable(command):
        command()
      else:
        os.system(command)
      time.sleep(delay_after)

@cli.command()
@click.argument('tpu', type=click.STRING, autocompletion=complete_tpu_id)
@click.option('--zone', type=click.Choice(tpudiepie.tpu.get_tpu_zones()))
@click.option('--version', type=click.STRING)
@click.option('-y', '--yes', is_flag=True)
@click.option('--dry-run', is_flag=True)
def delete(tpu, zone, version, yes, dry_run):
  tpu = tpudiepie.get_tpu(tpu=tpu, zone=zone)
  click.echo('Current status of TPU:')
  print_tpu_status_headers()
  print_tpu_status(tpu)
  click.echo('')
  delete = tpudiepie.delete_tpu_command(tpu, zone=zone)
  create = tpudiepie.create_tpu_command(tpu, zone=zone, version=version)
  def wait():
    wait_healthy(tpu, zone=zone)
  if not yes:
    print_step('Step 1: delete TPU.', delete)
    if not click.confirm('Proceed? {}'.format('(dry run)' if dry_run else '')):
      return
  do_step('Step 1: delete TPU...', delete, dry_run=dry_run)
  click.echo('TPU {} {} deleted.'.format(
    tpudiepie.tpu.parse_tpu_id(tpu),
    'would be' if dry_run else 'is'))
  print_step('You {} recreate the TPU with:'.format('could then' if dry_run else 'can'),
    create)

@cli.command()
@click.argument('tpu', type=click.STRING, autocompletion=complete_tpu_id)
@click.option('--zone', type=click.Choice(tpudiepie.tpu.get_tpu_zones()))
@click.option('--version', type=click.STRING)
@click.option('-y', '--yes', is_flag=True)
@click.option('--dry-run', is_flag=True)
def reimage(tpu, zone, version, yes, dry_run):
  tpu = tpudiepie.get_tpu(tpu=tpu, zone=zone)
  reimage = tpudiepie.reimage_tpu_command(tpu, version=version)
  def wait():
    wait_healthy(tpu, zone=zone)
  if not yes:
    print_step('Step 1: reimage TPU.', reimage)
    print_step('Step 2: wait until TPU is HEALTHY.', wait)
    if not click.confirm('Proceed? {}'.format('(dry run)' if dry_run else '')):
      return
  do_step('Step 1: reimage TPU...', reimage, dry_run=dry_run)
  do_step('Step 2: wait for TPU to become HEALTHY...', wait, dry_run=dry_run)
  click.echo('TPU {} {} ready for training.'.format(
    tpudiepie.tpu.parse_tpu_id(tpu),
    'would be' if dry_run else 'is'))

@cli.command()
@click.argument('tpu', type=click.STRING, autocompletion=complete_tpu_id)
@click.option('--zone', type=click.Choice(tpudiepie.tpu.get_tpu_zones()))
@click.option('--version', type=click.STRING)
@click.option('-y', '--yes', is_flag=True)
@click.option('--dry-run', is_flag=True)
def recreate(tpu, zone, version, yes, dry_run):
  tpu = tpudiepie.get_tpu(tpu=tpu, zone=zone)
  click.echo('Current status of TPU:')
  print_tpu_status_headers()
  print_tpu_status(tpu)
  click.echo('')
  delete = tpudiepie.delete_tpu_command(tpu, zone=zone)
  create = tpudiepie.create_tpu_command(tpu, zone=zone, version=version)
  def wait():
    wait_healthy(tpu, zone=zone)
  if not yes:
    print_step('Step 1: delete TPU.', delete)
    print_step('Step 2: create TPU.', create)
    print_step('Step 3: wait until TPU is HEALTHY.', wait)
    if not click.confirm('Proceed? {}'.format('(dry run)' if dry_run else '')):
      return
  do_step('Step 1: delete TPU...', delete, dry_run=dry_run)
  do_step('Step 2: create TPU...', create, dry_run=dry_run)
  do_step('Step 3: wait for TPU to become HEALTHY...', wait, dry_run=dry_run)
  click.echo('TPU {} {} ready for training.'.format(
    tpudiepie.tpu.parse_tpu_id(tpu),
    'would be' if dry_run else 'is'))

def main(*args, prog_name='tpudiepie', auto_envvar_prefix='TPUDIEPIE', **kws):
  cli.main(*args, prog_name=prog_name, auto_envvar_prefix=auto_envvar_prefix, **kws)

if __name__ == "__main__":
  main()

