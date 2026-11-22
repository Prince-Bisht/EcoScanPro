from pathlib import Path
import json,os,requests
KB=json.loads((Path(__file__).resolve().parents[1]/'data'/'waste_guidelines.json').read_text())
def answer(message,history=None):
    key=os.getenv('LLM_API_KEY','').strip()
    if key:
        try:
            base=os.getenv('LLM_BASE_URL','https://api.openai.com/v1').rstrip('/')
            context='\n'.join(f'{k}: {v}' for k,v in KB.items())
            msgs=[{'role':'system','content':'You are Eco AI, an environmental education assistant. Ground answers in the following knowledge base where applicable; distinguish local rules and uncertainty.\n'+context}]
            for item in (history or [])[-10:]:
                if isinstance(item,dict) and item.get('role') in ('user','assistant') and isinstance(item.get('content'),str): msgs.append({'role':item['role'],'content':item['content'][:2000]})
            msgs.append({'role':'user','content':message})
            r=requests.post(base+'/chat/completions',headers={'Authorization':'Bearer '+key},json={'model':os.getenv('LLM_MODEL','gpt-4o-mini'),'messages':msgs},timeout=18)
            r.raise_for_status()
            return {'response':r.json()['choices'][0]['message']['content'],'mode':'llm'}
        except Exception: pass
    words=message.lower()
    aliases={'biodegradable':['biodegradable','organic'],'plastic':['plastic'],'segregation':['segregat','wet waste','dry waste'],'compost':['compost'],'e-waste':['e-waste','electronic','battery'],'recycling':['recycl'],'india':['india','municipal'],'pollution':['pollut','burning'],'ai':['artificial intelligence','machine learning','ai ']}
    matches=[KB[k] for k,keys in aliases.items() if any(w in words for w in keys)]
    response=' '.join(matches[:2]) if matches else 'I can help with plastic recycling, composting, segregation, e-waste and sustainable habits. Please ask about one of these topics. I cannot verify city-specific collection rules.'
    return {'response':response,'mode':'knowledge-base-fallback','notice':'Offline curated knowledge-base response, not a live LLM answer.'}
