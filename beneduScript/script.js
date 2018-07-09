

        var IBT_ID;
        var IBQ_ID;
        var IBU_BEGIN_DATE;
        var IBU_BEGIN_TIME;

        $(document).ready(function () {
            $('#mnu03StdStudy').addClass('active');

            $("#btnSubmit").click(function () {

                if (typeof (grecaptcha) != 'undefined') {
                    if (grecaptcha.getResponse() == "") {
                        Show_Alert('캡차를 체크해 주세요.', '캡차 체크누락');
                        return;
                    }
                }

                document.getElementById('body_txtAnswers').value = "";

                // 문제 수
                var QST_Cnt = 0;
                // 시작 IBQ_NUM
                var First_Num = 0;

                for (var i = 1 ; i < 201 ; i++) {

                    var btnID = "btn_" + i + "_1";

                    if (document.getElementById(btnID) != null) {
                        QST_Cnt++;

                        if (First_Num == 0) {
                            First_Num = i;
                        }
                    }
                }

                // 선택 확인
                for (var i = First_Num ; i < First_Num + QST_Cnt ; i++) {

                    var IsChecked = false

                    var objectID = "btn_" + i + "_1";

                    if (document.getElementById(objectID).getAttribute('data-essay_yn') == 'Y') {
                        // 주관식
                        if (document.getElementById(objectID).value != '') {
                            IsChecked = true;
                            document.getElementById('body_txtAnswers').value += document.getElementById(objectID).getAttribute('data-QST_ID') + "_" + i + "_" + document.getElementById(objectID).value + "/";
                        }
                    }
                    else {
                        // 객관식
                        for (var j = 0 ; j < 5 ; j++) {

                            var btnID = "btn_" + i + "_" + (j + 1);

                            if (document.getElementById(btnID) != null) {

                                if (document.getElementById(btnID).className == "badge bg_blue") {
                                    IsChecked = true;
                                    document.getElementById('body_txtAnswers').value += document.getElementById(btnID).getAttribute('data-QST_ID') + "_" + i + "_" + (j + 1) + "/";
                                    break;
                                }
                            }
                        }
                    }

                    var ckb = "ckb_" + i;

                    if (IsChecked == false && document.getElementById(ckb).value == "N") {
                        Show_Alert('체크하지않은 답안이 있습니다. 확인해주세요.', '시험 응시');
                        return;
                    }
                    else if (IsChecked == false && document.getElementById(ckb).value == "Y") {
                        if (document.getElementById(objectID).getAttribute('data-essay_yn') == 'Y') {
                            document.getElementById('body_txtAnswers').value += document.getElementById(objectID).getAttribute('data-QST_ID') + "_" + i + "_ /";
                        }
                        else {
                            document.getElementById('body_txtAnswers').value += document.getElementById(btnID).getAttribute('data-QST_ID') + "_" + i + "_0/";
                        }
                    }

            }

                document.getElementById('body_txtAnswers').value += QST_Cnt;

                


                //fnShowMacroForm();
                __doPostBack('ctl00$body$lnkSubmit', IBT_ID + '＃' + IBQ_ID + '＃' + IBU_BEGIN_DATE + '＃' + IBU_BEGIN_TIME);

            });

            $("#btnMoveList").click(function () {

                var Val = document.getElementById('btnMoveList').value;

                if (Val == "01") {
                    window.location.assign("03StdStudy02PaperTestList.aspx");
                }
                else if (Val == "02") {
                    window.location.assign("03StdStudy04Homework.aspx");
                }
                else if (Val == "03") {
                    window.location.assign("03StdStudy03Recommend.aspx");
                }

            });

            $("#btnView").click(function () {

                Show_Loading_Short();

                var quizCnt = document.getElementById('body_hQuizCnt').value;    
                var type3ID = 'Table_ExamType3_';

                if (document.getElementById('btnView').value == 1) {

                    document.getElementById('Table_Exame').className = "table table-bordered table-hover table_ex Font_Exam";
                    document.getElementById('Table_ExamType2Print').className = "table table-bordered table-hover table_ex Font_Exam";
                    document.getElementById('Table_ExamType2Quiz').className = "table table-bordered table-hover table_ex Font_Exam";

                    for (var i = 0; i < quizCnt; i++) {

                        var nowID = type3ID + i.toString();

                        document.getElementById(nowID).className = "table table-bordered table-hover table_ex Font_Exam";

                    }

                    document.getElementById('btnView').value = 0;
                    document.getElementById('btnView').innerHTML = '<img style="width:18px; margin-bottom:3px;" alt="" src="../../Contents/Image/ico/FontChange_icon.png"><span>&nbsp; 고어체 표시</span> '

                }
                else {

                    document.getElementById('Table_Exame').className = "table table-bordered table-hover table_ex Font_Naver";
                    document.getElementById('Table_ExamType2Print').className = "table table-bordered table-hover table_ex Font_Naver";
                    document.getElementById('Table_ExamType2Quiz').className = "table table-bordered table-hover table_ex Font_Naver";

                    for (var i = 0; i < quizCnt; i++) {

                        var nowID = type3ID + i.toString();

                        document.getElementById(nowID).className = "table table-bordered table-hover table_ex Font_Naver";

                    }

                    document.getElementById('btnView').value = 1;
                    document.getElementById('btnView').innerHTML = '<img style="width:18px; margin-bottom:3px;" alt="" src="../../Contents/Image/ico/FontChange_icon.png"><span>&nbsp; 고어체 해제</span> '

                }

            });


            $("#btnSave").click(function () {

                document.getElementById('body_txtAnswers').value = "";

                // 문제 수
                var QST_Cnt = 0;
                // 시작 IBQ_NUM
                var First_Num = 0;

                for (var i = 1 ; i < 100 ; i++) {

                    var btnID = "btn_" + i + "_1";

                    if (document.getElementById(btnID) != null) {
                        QST_Cnt++;

                        if (First_Num == 0) {
                            First_Num = i;
                        }
                    }
                }

                // 선택 확인
                for (var i = First_Num ; i < First_Num + QST_Cnt ; i++) {

                    var IsChecked = false

                    var objectID = "btn_" + i + "_1";

                    if (document.getElementById(objectID).getAttribute('data-essay_yn') == 'Y') {
                        // 주관식
                        if (document.getElementById(objectID).value != '') {
                            IsChecked = true;
                            document.getElementById('body_txtAnswers').value += document.getElementById(objectID).getAttribute('data-QST_ID') + "_" + i + "_" + document.getElementById(objectID).value + "/";
                        }
                    }
                    else {
                        // 객관식
                        for (var j = 0 ; j < 5 ; j++) {

                            var btnID = "btn_" + i + "_" + (j + 1);

                            if (document.getElementById(btnID) != null) {

                                if (document.getElementById(btnID).className == "badge bg_blue") {
                                    IsChecked = true;
                                    document.getElementById('body_txtAnswers').value += document.getElementById(btnID).getAttribute('data-QST_ID') + "_" + i + "_" + (j + 1) + "/";
                                    break;
                                }
                            }
                        }
                    }

                    var ckb = "ckb_" + i;

                    if (IsChecked == false && document.getElementById(ckb).value == "Y") {
                        if (document.getElementById(objectID).getAttribute('data-essay_yn') == 'Y') {
                            document.getElementById('body_txtAnswers').value += document.getElementById(objectID).getAttribute('data-QST_ID') + "_" + i + "_ /";
                        }
                        else {
                            document.getElementById('body_txtAnswers').value += document.getElementById(btnID).getAttribute('data-QST_ID') + "_" + i + "_0/";
                        }
                    }

                }

                __doPostBack('ctl00$body$lnkSave', IBT_ID + '＃' + IBQ_ID + '＃' + IBU_BEGIN_DATE + '＃' + IBU_BEGIN_TIME);

            });





            // ViewType 관련 Start

            // radio change 이벤트
            $("input[name=radioName]").change(function () {

                var radioValue = $(this).val();

                if (radioValue == "viewType1") {

                    document.getElementById('examPrevBtn').style.display = "none";
                    document.getElementById('examNextBtn').style.display = "none";
                    document.getElementById('body_hdViewType').value = "viewType1";
                    showExclude("examViewType1");

                } else if (radioValue == "viewType2") {

                    document.getElementById('examPrevBtn').style.display = "none";
                  …