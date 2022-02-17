import click

from git_summarizer import process_repo


@click.group(chain=True)
@click.pass_context
def cli(ctx):
    pass


@cli.command()
@click.option('--repo_type',
              prompt='Type one of option names',
              type=click.Choice(["url", "directory"]),
              show_default=False)
@click.pass_context
def get_repo_type(ctx, repo_type):
    click.echo(f"Program will analyze sources from {repo_type}")
    ctx.obj['TYPE'] = repo_type


@cli.command()
@click.option('--url',
              prompt='Type URL of remote repository (skip with ENTER for directory option)',
              default="Press ENTER for directory option")
@click.pass_context
def get_repo_url(ctx, url):
    if ctx.obj['TYPE'] == 'url':
        click.echo(f"Received repo: {url}")
        ctx.obj['URL'] = url


@cli.command()
@click.option('--dir',
              prompt='Enter path to directory',
              type=click.Path())
@click.pass_context
def get_directory(ctx, dir):
    click.echo(f"Path to repo directory: {dir}")
    ctx.obj['DIR'] = dir
    if 'URL' in ctx.obj.keys():
        process_repo(repo=ctx.obj['DIR'], url=ctx.obj['URL'])
    else:
        process_repo(repo=ctx.obj['DIR'])


if __name__ == '__main__':
    cli(obj={})
