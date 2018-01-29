from bottle import route, get, request, run, template, static_file, abort, Bottle, response
import json
import ast
import pg_logger
import missionConfig
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = application = Bottle()


# codeStr = 'monkey.step(10)\ngoat.hit()\nmonkey.turn(15)\nmonkey.goto(bananas[0])\nfor m in monkeys:\n    m.turn(15)\n'


def allow_cross_domain(fn):
    def _enable_cross(*args, **kwargs):
        # Set cross headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,OPTIONS'
        allow_headers = 'Referer, Accept, Origin, User-Agent'
        response.headers['Access-Control-Allow-Headers'] = allow_headers
        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cross

@app.route('/<filepath:path>')
@allow_cross_domain
def index(filepath):
    return static_file(filepath, root='.')


@app.get('/runscript')
@allow_cross_domain
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
        # print(missionInfo)
        pass
    else:
        # outString.write('Get mission info error!')
        # return outString.getvalue()
        abort(404, 'Get mission info error!')
    userCode = 'from gameObj import *\ninit("{0}")\n'.format(missionNum)+request.query.usercode
    #print(userCode)
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
            '''
            execinfo = 'instruction_limit_reached.Stopped after running 1000 steps. Please shorten your code,\n'
            execinfo += 'since Python Tutor is not designed to handle long-running code.'
            '''
            execinfo = 'OVERFLOW'
            respData = {'line': 1, 'command': codeList[2], 'execinfo': execinfo}
            respList.append(respData)
            outTrace = []

        for linedata in outTrace:
            if len(outTrace) < 1:
                continue
            # print(linedata)
            lNum = linedata['line']-2
            commStr = codeList[lNum+1].strip()
            execinfo = 'OK'
            execerror = False
            respData = {}

            if (linedata['event'] == 'exception') or (linedata['event'] == 'uncaught_exception'):
                execinfo = linedata['exception_msg']
                execerror = True
                respData = {'line': lNum, 'command': commStr, 'execinfo': execinfo}

            elif (linedata['event'] == 'call'):
                respList.pop(-1)
            elif (commStr[:5] == 'class'):
                respData = {'line': lNum, 'command': commStr, 'execinfo': "Class was not supported..."}
            elif (commStr[-1:] == ':'):
                pass
            elif (len(linedata['globals']) < 2):
                pass
                #print(commStr)
            else:
                #print(commStr)
                globals = linedata['globals']
                heap = linedata['heap']
                # encoded_locals = linedata['encoded_locals']
                stack_to_render = linedata['stack_to_render']
                func_name = linedata['func_name']

                codeNode = ast.parse(commStr)
                nodeList = ast.walk(codeNode)
                for node in nodeList:
                    if isinstance(node, ast.Name):
                        #print(node.id)
                        try:
                            nodeProper = stack_to_render[0]['encoded_locals'][node.id]
                        except:
                            try:
                                nodeProper = globals[node.id]
                            except Exception as e:
                                print(repr(e))
                                continue
                        try:
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
                            print('Get NodeName Error: {0}'.format(e))

                #print(commStr)
                respData = {'line': lNum, 'command': commStr, 'execinfo': execinfo}
            if (len(respData) > 0) and (lNum > 0) and (linedata['event'] != 'return'):
                respList.append(respData)
        #outString.write(json.dumps(outTrace, ensure_ascii=False))
        respList.append({'line': -1, 'command': 'commandEnd()', 'execinfo': 'END'})
        outString.write(json.dumps(respList,ensure_ascii=False))

    pg_logger.exec_script_str_local(userCode,'',False,False,recvTrace)
    #outString.write(userCode)
    return outString.getvalue()



if __name__ == '__main__':
    # codeStr = 'from gameObj import *\ninit(0)\n' + codeStr
    #pg_logger.exec_script_str_local(codeStr, '', False, False, recvTrace)
    run(application, host='127.0.0.1', port=8888, reloader=True)
