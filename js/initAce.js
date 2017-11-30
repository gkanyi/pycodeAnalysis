$(function(){
    function init() {
        initAce();
    }
    function initAce() {
        var codeEditor = ace.edit("codeInputPane");
        var codeSession = codeEditor.getSession();
        codeSession.setTabSize(4);
        codeSession.setUseSoftTabs(true);
        codeSession.getDocument().setNewLineMode('unix');
        codeSession.setMode("ace/mode/python");
        codeEditor.setHighlightActiveLine(true);
        codeEditor.setShowPrintMargin(false);
        codeEditor.setBehavioursEnabled(false);
        codeEditor.setOptions({minLines: 30, maxLines: 1000});
        codeEditor.setValue("Input python code...");
        codeEditor.commands.addCommand({
            name: 'RunCode',
            bindKey:  {win: 'Ctrl-R',  mac: 'Command-R'},
            exec: function (codeEditor) {
                console.log(codeEditor.getValue());
                var mNum = $("#mission").val();
                console.log(mNum);
                runUrl = 'http://pycode.raccooncode.com/runscript';
                runData = {
                    usercode: codeEditor.getValue(),
                    mission: mNum.toString()
                };
                $.get(runUrl, runData, function (result) {
                    console.log(result);
                });
            }
        });

    }
    init();
})
