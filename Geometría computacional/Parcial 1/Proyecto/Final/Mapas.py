import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def lista_bords2map(v, bordes, vc='b', bc='k'):
    twins=[]
    plt.axis('off')
    plt.scatter(np.array(v.x), np.array(v.y), c=vc)
    for i, bo in bordes.iterrows():
        if not i in twins:
            vin = bo['vert_or']
            vfi = bordes.loc[bo['twin']]['vert_or']
            twins.append(bo['twin'])
            plt.plot( [v.loc[vin]['x'], v.loc[vfi]['x']], [v.loc[vin]['y'], v.loc[vfi]['y']], c=bc)
    plt.show()

def lista_semibordes_ext(f, caras, bordes):
    way = []
    if caras.loc[f]['b_ext'] != None:
        val = "'" + str(f) + "'"
        sent = 'f==' + val
        qr = bordes.query(sent)
        e = caras.loc[f]['b_ext']
        way.append(e)
        e1 = qr.loc[e]['next']
        while (e1 != e):
            way.append(e1)
            e1 = qr.loc[e1]['next']
    else:
        way= None
    return way
    
def lista_semibordes_int(f, caras, bordes):
    fi = []
    arr = caras.loc[f]['b_int']
    way = []
    if arr:
        val = "'" + str(f) + "'"
        sent = 'f==' + val
        qr = bordes.query(sent)
        for w in arr:
            e = w
            way.append(e)
            e1 = qr.loc[e]['next']
            while (e1 != e):
                way.append(e1)
                e1 = qr.loc[e1]['next']
            fi.append(way)
            way = []
    else:
        fi= []
    return fi

def lista_semibordes_vertice(vt, v, bordes):
    bor = []
    e = v.loc[vt]['b']
    bor.append(e)
    e1 = bordes.loc[bordes.loc[e]['twin']]['next']
    while (e1 != e):
        bor.append(e1)
        e1 = bordes.loc[bordes.loc[e1]['twin']]['next']
    return bor

def map_cara(f, caras, bordes, v, inter='b', exter='r'):
    pa = []
    plt.axis('off')
    plt.scatter(np.array(v.x), np.array(v.y), c='k')
    if caras.loc[f]['b_ext'] != None:
        ext = lista_semibordes_ext(f, caras, bordes)
        xmi=np.inf; xma=-1*np.inf; ymi=np.inf; yma=-1*np.inf;
        n=1
        for ex in ext:
            x1 = v.loc[bordes.loc[ex]['vert_or']]['x']
            x2 = v.loc[bordes.loc[bordes.loc[ex]['twin']]['vert_or']]['x']
            y1 = v.loc[bordes.loc[ex]['vert_or']]['y']
            y2 = v.loc[bordes.loc[bordes.loc[ex]['twin']]['vert_or']]['y']
            plt.plot([x1, x2], [y1, y2],c=inter)
            plt.text( float(x1+x2)/2, float(y1+y2)/2, str(n), fontsize=10)
            n+=1
            pa.extend([ ex , bordes.loc[ex]['twin'] ])
            x1, x2 = (x1, x2) if (x1<x2) else (x2, x1)
            y1, y2 = (y1, y2) if (y1<y2) else (y2, y1)
            xmi = (x1) if (x1<xmi) else (xmi)
            xma = (x2) if (x2>xma) else (xma)
            ymi = (y1) if (y1<ymi) else (ymi)
            yma = (y2) if (y2>yma) else (yma)
        plt.text( float(xmi+xma)/2, float(ymi+yma)/2, str(f), fontsize=10)
    if caras.loc[f]['b_int']:
        inte = lista_semibordes_int(f, caras, bordes)
        for row in inte:
            n = 1
            for cel in row:
                x1 = v.loc[bordes.loc[cel]['vert_or']]['x']
                x2 = v.loc[bordes.loc[bordes.loc[cel]['twin']]['vert_or']]['x']
                y1 = v.loc[bordes.loc[cel]['vert_or']]['y']
                y2 = v.loc[bordes.loc[bordes.loc[cel]['twin']]['vert_or']]['y']
                plt.plot([x1, x2], [y1, y2],c=exter)
                plt.text( float(x1+x2)/2, float(y1+y2)/2, str(n), fontsize=10)
                n+=1
                pa.extend([ cel , bordes.loc[cel]['twin'] ])
    for i, bo in bordes.iterrows():
        if not i in pa:
            vin = bo['vert_or']
            vfi = bordes.loc[bo['twin']]['vert_or']
            pa.append(bo['twin'])
            plt.plot( [v.loc[vin]['x'], v.loc[vfi]['x']], [v.loc[vin]['y'], v.loc[vfi]['y']], c='k')
    plt.show() 
    
def map_brds_vert(vo, v, bordes, cb='r'):
    pa = []
    plt.axis('off')
    plt.scatter(v.x, v.y, c='k')
    smbo = lista_semibordes_vertice(vo, v, bordes)
    for sb in smbo:
        vin = bordes.loc[sb]['vert_or']
        vfi = bordes.loc[bordes.loc[sb]['twin']]['vert_or']
        plt.plot([ v.loc[vin]['x'], v.loc[vfi]['x'] ],[ v.loc[vin]['y'], v.loc[vfi]['y'] ], c=cb)
        pa.extend([sb, bordes.loc[sb]['twin']])
    for i, bo in bordes.iterrows():
        if not i in pa:
            vin = bo['vert_or']
            vfi = bordes.loc[bo['twin']]['vert_or']
            pa.append(bo['twin'])
            plt.plot( [v.loc[vin]['x'], v.loc[vfi]['x']], [v.loc[vin]['y'], v.loc[vfi]['y']], c='k')
    plt.show()
