#!/usr/bin/env python3

import openai
from openai import OpenAI
import os
import typer
import dotenv
import toml
import json
import re

# Global state  ----------------------------------------------------------------
app = typer.Typer()

dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv('API_KEY'))
# ------------------------------------------------------------------------------

@app.command(name='convo')
def args_convo(
        agent: str  = typer.Argument(),
        prompt: str = typer.Argument(),
        agentfile: str = typer.Option(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "agents.toml")
        ),
        sep0: str = typer.Option('* '),
        sep1: str = typer.Option(' '),
        sep2: str = typer.Option('─'),
        sep3: str = typer.Option('*'),
        sepl: int = typer.Option(80),
): convo(locals())
def convo(args):
    agent = toml.load(args['agentfile'])[args['agent']]

    chat_args = agent['settings']
    chat_args['messages'] = [
        {'role': 'system', 'content' : agent['system_msg']}
    ] + parse_prompt(args)

    stream = client.chat.completions.create(**chat_args)

    sep_agent = args['sepl'] - len(args['sep0']) - len(args['agent']) - len(args['sep1']) - len(args['sep3'])
    sep_user = args['sepl'] - len(args['sep0']) - len('user') - len(args['sep1']) - len(args['sep3'])

    # Print separation line
    print()
    print(args['sep0']
          + args['agent']
          + args['sep1']
          + args['sep2']*int(sep_agent/len(args['sep2']))
          + args['sep3'])

    # Print model stream
    for chunk in stream:
        if chunk.choices[0].delta.content is not None: # Question: what are choices? chunk.choices[0]
            print(chunk.choices[0].delta.content, end='')
    
    # Print separation line
    print()
    print(args['sep0']
          + 'user'
          + args['sep1']
          + args['sep2']*int(sep_user/len(args['sep2']))
          + args['sep3'], end='')
def parse_prompt(args):
    lines = args['prompt'].split('\n')
    tokens = [tokenize(line,
                       sep0=args['sep0'],
                       sep1=args['sep1'],
                       sep2=args['sep2'],
                       sep3=args['sep3'],) for line in lines]

    for token in tokens:
        if token['type'] == 'role' and token['value'] not in ['user', 'system']:
            token['value'] = 'assistant'
    
    if tokens[0]['type'] != 'role':
        tokens.insert(0, {
            'type': 'role',
            'value': 'user',
        })
       
    convo = aggregate(tokens)
    
    return convo#[{'role': 'user', 'content': args['prompt']}]
def tokenize(line, sep0='* ', sep1=' ', sep2='-', sep3=' o'):
    r = lambda s: ''.join(reversed(s))        
    regex = re.escape(r(sep3)) + re.escape(r(sep2)) + '+' + re.escape(r(sep1)) + '(.*?)' + re.escape(r(sep0))
    
    matches = re.search(regex, r(line))
    if not matches: return {
            'type': 'line',
            'value': line,
    }
    
    return {
        'type': 'role',
        'value': r(matches.group(1)),
    }
def aggregate(tokens):
    convo =  []    
    for token in tokens:
        if token['type'] == 'role':            
            convo.append({
                'role': token['value'],
                'content': '',
            })
        elif token['type'] == 'line':
            convo[-1]['content'] += token['value'] + '\n'
            
    return convo

@app.command(name="agents", help="List available GPT agents")
def agents(
        agents: str  = typer.Option(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "agents.toml")
        ),
):
    print(" ".join(agent for agent in sorted(toml.load(agents))))

@app.command(name='test')
def test():
    print('Test')

if __name__ == '__main__': app()
        
