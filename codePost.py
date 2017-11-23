from bottle import route, get, request, run, template, static_file
import json
import ast
import pg_logger
import missionConfig
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


codeStr = 'monkey.step(10)\ngoat.hit()\nmonkey.turn(15)\nmonkey.goto(bananas[0])\nfor m in monkeys:\n    m.turn(15)\n'

@route('/<filepath:path>')
def index(filepath):
    # special-case for testing name_lookup.py ...
    if 'name_lookup.py' in filepath:
        return json.dumps(dict(name='TEST NAME', email='TEST EMAIL'))
    return static_file(filepath, root='.')

@get('/runscript')
def runscript():
    outString = StringIO()
    try:
        missionNum = str(request.query.mission)
    except:
        missionNum = '0'

    try:
        missionInfo = missionConfig.missionInfo[missionNum]
    except:
        missionInfo = None
    if isinstance(missionInfo,list):
        print(missionInfo)
    else:
        outString.write('Get mission info error!')
        return outString.getvalue()
    userCode = 'from gameObj import *\ninit("{0}")\n'.format(missionNum)+request.query.usercode
    print(userCode)
    codeList = userCode.split('\n')
    mission = request.query.mission
    respList = []

    def recvTrace(inputCode, outTrace):
        # print(inputCode)
        codeList = inputCode.split('\n')
        '''
        for i, codeLine in enumerate(codeList):
            print('{0}:{1}'.format(i, codeLine))
        '''
        if len(outTrace) > 998:
            execerror = True
            execinfo = 'instruction_limit_reached.Stopped after running 1000 steps. Please shorten your code,\n'
            execinfo += 'since Python Tutor is not designed to handle long-running code.'
            respData = {'line': 1, 'command': codeList[2], 'execinfo': execinfo}
            respList.append(respData)
            outTrace = []

        for linedata in outTrace:
            if len(outTrace) < 1:
                continue
            print(linedata)
            lNum = linedata['line']-2
            commStr = codeList[lNum+1].strip()
            execinfo = 'OK'
            execerror = False
            respData = {}

            if (linedata['event'] == 'exception') or (linedata['event'] == 'uncaught_exception'):
                execinfo = linedata['exception_msg']
                execerror = True
                respData = {'line': lNum, 'command': commStr, 'execinfo': execinfo}

            elif (commStr[-1:] == ':'):
                pass
            elif (len(linedata['globals']) < 2):
                pass
                #print(commStr)
            else:
                #print(commStr)
                globals = linedata['globals']
                heap = linedata['heap']

                codeNode = ast.parse(commStr)
                nodeList = ast.walk(codeNode)
                for node in nodeList:
                    if isinstance(node, ast.Name):
                        #print(node.id)
                        try:
                            nodeProper = globals[node.id]
                            if isinstance(nodeProper,list):
                                nodeName = heap[nodeProper[-1]]
                                #print(nodeName)
                                if nodeName[0] == 'INSTANCE':
                                    #print(nodeName[-1][-1])
                                    #print(commStr,node.id,nodeName[-1][-1],type(commStr))
                                    commName = ''
                                    for c in nodeName:
                                        if isinstance(c, list):
                                            if c[0] == 'name':
                                                commName = c[-1]
                                    commStr = commStr.replace(node.id+'.',commName+'.')
                                    commStr = commStr.replace(node.id + ')', commName + ')')
                                    #print(commStr)
                        except Exception as e:
                            print(e)
                #print(commStr)
                respData = {'line': lNum, 'command': commStr, 'execinfo': execinfo}
            if (len(respData) > 0) and (lNum > 0) and (linedata['event'] != 'return'):
                respList.append(respData)
        #outString.write(json.dumps(outTrace, ensure_ascii=False))
        outString.write(json.dumps(respList,ensure_ascii=False))

    pg_logger.exec_script_str_local(userCode,'',False,False,recvTrace)
    #outString.write(userCode)
    return outString.getvalue()



if __name__ == '__main__':
    codeStr = 'from gameObj import *\ninit(0)\n' + codeStr
    #pg_logger.exec_script_str_local(codeStr, '', False, False, recvTrace)
    run(host='127.0.0.1', port=8888,reloader=True)