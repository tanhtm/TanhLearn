function $E(e) { if (!e) return 0; return e.tagName ? e : document.getElementById(e) || 0; } function $T(e, t, i) { var a = $E(e); if (!a) return 0; a = a.getElementsByTagName(t || '*'); if (i != 0 && !i) return (a || 0); return (i < 0 || i >= a.length) ? 0 : a[i]; } function $C(e, c, t, i) { var a = $E(e); var b = []; if (!t) t = '*'; if (!a) return 0; if (!c) return $T(e, t, i); if (a.getElementsByClassName) { a = a.getElementsByClassName(c); for (var j = 0; j < a.length; j++) { if (t == '*' || a[i].tagName == t.toUpperCase()) b.push(a[j]); } } else { b = a.getElementsByTagName(t); for (var j = 0; j < a.length; j++) { if (c && a[i].className.indexOf(c) < 0) continue; b.push(a[i]); } } if (i != 0 && !i) return b; return (i < 0 || i >= b.length) ? 0 : b[i]; }
var __evt = { click: [], load: [], resize: [], scroll: [], responsive: [], call: function (n) { n = n.toString(); if (n && n != 'call' && this[n]) { var e = window.events || arguments[0], f = this[n]; for (var i = 0; i < f.length; i++) { if (f[i]) { try { f[i](e); } catch (ex) { } } } } } };
function Handle(n, f) { n = n.toString(); if (n && n != 'call' && __evt[n]) { __evt[n].push(f); } } window.onclick = function () { __evt.call('click'); }; window.onload = function () { __evt.call('load'); }; window.onresize = function () { __evt.call('resize'); }; window.onscroll = function () { __evt.call('scroll'); };

function PopAlarm(e, m, t) {
    e = $E(e); if (!e) return 0;
    e.msg = $C(e, 'alertbox', '', 0); if (!e.msg) return 0;
    e.txt = $C(e.msg, 'message', '', 0); if (!e.txt) return 0;
    e.cls = $C(e.msg, 'closing', '', 0); if (!e.cls) return 0;
    e.Pop = function (c) { e.style.display = c ? 'block' : 'none'; e.msg.style.display = c ? 'block' : 'none'; };
    e.cls.onclick = function () { e.Pop(0); t.focus(); };

    e.txt.innerHTML = m;
    e.Pop(1);
    return e;
};
function CommentPanelr(e, v) {
    e = $E(e); if (!e) return 0; e.vwr = $E(v); if (!e.vwr) return 0;
    e.btn = $C(e, 'confirmer', '', 0); if (!e.btn) return 0;
    e.txt = $C(e, 'message', '', 0); if (!e.txt) return 0;
    e.con = $C(e.vwr, 'comm_confirm', '', 0); if (!e.con) return 0;
    e.snd = $C(e.con, 'sending', '', 0); e.cls = $C(e.con, 'closing', '', 0);
    e.hid = $C(e.con, 'hidmsg', '', 0);
    e.Pop = function (c, m, p) { e.vwr.style.display = c ? 'block' : 'none'; e.con.style.display = c ? 'block' : 'none'; if (e.hid && m) { e.hid.value = m; } if (p) { e.hid.form.action = p; } };
    e.btn.onclick = function () {
        if (!e.txt.value || e.txt.value.length < 15 || e.txt.value.length > 4000) {
            PopAlarm(v, 'Nội dung bình luận không hợp lệ! Vui lòng nhập lại. 1', e.txt);
            return false;
        }
        e.Pop(1, e.txt.value, e.txt.form.action);
        return false;
    };
    e.txt.onfocus = function () { if (!e.txt.title) { e.txt.title = e.txt.value; e.txt.value = ''; } };
    e.txt.onblur = function () { if (!e.txt.value) { e.txt.value = e.txt.title; e.txt.title = ''; } };
    if (e.snd) { e.snd.onclick = function () { e.txt.value = e.txt.title; e.txt.title = ''; }; }
    if (e.cls) { e.cls.onclick = function () { e.Pop(0); }; }

    e.rep = $C(e, 'replybox', '', 0);
    if (e.rep) {
        e.btm = $C(e.rep, 'vwmor', '', 0);
        e.mor = $C(e.rep, 'morcomments', '', 0);
        if (e.mor && e.btm) { e.btm.onclick = function () { e.mor.style.display = ''; e.btm.style.display = 'none'; return false; }; }

        e.rbf = $C(e.rep, 'replyform', '', 0);
        e.rbs = [];
        var rl = $T(e.rep, 'li');
        if (e.rbf && rl) {
            for (var i = 0; i <= rl.length; i++) {
                var rb = $C(rl[i], 'irep', '', 0);
                if (rb) {
                    rb.par = rl[i];
                    rb.onclick = function () {
                        var p = this.par; if (!p) return false; p.appendChild(e.rbf); e.rbf.action = this.href; e.rbf.style.display = '';
                        var rms = $C(e.rbf, 'replying', '', 0), rsn = $C(e.rbf, 'replier', '', 0), rcl = $C(e.rbf, 'repcloser', '', 0);
                        rms.onfocus = function () { if (!this.title) { this.title = this.value; this.value = ''; } };
                        rms.onblur = function () { if (!this.value) { this.value = this.title; this.title = ''; } };
                        if (rsn) {
                            rsn.onclick = function () {
                                if (!rms.value || rms.value.length < 15 || !rms.title || rms.value.length > 4000) {
                                    PopAlarm(v, 'Nội dung trả lời không hợp lệ! Vui lòng nhập lại.', rms);
                                    return false;
                                }
                                e.Pop(1, rms.value, rms.form.action);
                                return false;
                            };
                        }
                        if (rcl) { rcl.onclick = function () { rms.value = rms.title; rms.title = ''; e.rbf.style.display = 'none'; return false; }; }
                        return false;
                    };
                    e.rbs.push(rb);
                }
            }
        }
    }
    return e;
};
var commConf = CommentPanelr('CommentBox', 'PopViewrComment');
function PhotoAlbum(e) {
    e = $E(e); if (!e) return 0; e.cur = 0; e.tmr = 0; e.itr = 0;
    e.pto = $C(e, 'preview', '', 0); e.alb = $C(e, 'album', '', 0); if (!e.pto || !e.alb) return 0;
    e.inf = $C(e.pto, 'inf', '', 0); e.clk = $C(e.pto, 'clk', '', 0); e.pto = $T(e.pto, 'img', 0);
    e.sld = $T(e.alb, 'ul', 0); e.itm = $T(e.sld, 'a');
    if (!e.pto || !e.alb || !e.sld || !e.itm.length) return 0;
    if (e.inf) { e.def = $C(e.inf, 'def', '', 0); e.cnt = $C(e.inf, 'cnt', '', 0); }
    e.Start = function (a) { if (a) { e.tmr = setTimeout(e.Next, 5000); } else { if (e.tmr) { clearTimeout(e.tmr); e.tmr = 0; } } };
    e.Slide = function (i) { e.Start(0); var a = e.itm[i]; if (a) { e.pto.src = a.href; e.MoveTo(i); e.SetInf(a, i); e.itm[e.cur].className = ''; a.className = 'sel'; e.cur = i; } e.Start(1); };
    e.SetInf = function (a, i) { if (!e.inf) return; clearTimeout(e.itr); e.inf.style.height = '0px'; e.inf.style.marginTop = '0px'; e.itr = setTimeout(function () { if (e.def) { e.def.innerHTML = a.title; } if (e.cnt) { e.cnt.innerHTML = 'Ảnh thứ ' + (i + 1).toString() + ' trong ' + e.itm.length.toString() + (a.title ? ':' : '') } var p = $T(e.inf, 'p', 0); p = (p ? p.offsetHeight + 15 : e.inf.offsetHeight); e.inf.style.height = p.toString() + 'px'; e.inf.style.marginTop = '-' + p.toString() + 'px'; }, 500); };
    e.MoveTo = function (i) { var w = e.itm[0].offsetWidth + 5, n = e.alb.offsetWidth, m = e.itm.length * w - n, l = w * i; n = parseInt((n * 2) / 3); if (l < n) { l = 0; } if (l > m) { l = m; } e.sld.style.marginLeft = '-' + l.toString() + 'px'; }
    e.Next = function () { var i = e.cur + 1; if (i >= e.itm.length) { i = 0; } e.Slide(i); };
    e.Prev = function () { var i = e.cur - 1; if (i < 0) { i = e.itm.length - 1; } e.Slide(i); };
    for (var i = 0; i < e.itm.length; i++) { e.itm[i].onclick = function () { for (var i = 0; i < e.itm.length; i++) { if (e.itm[i] == this) { e.Slide(i); return false; } } return false; }; }
    if (e.clk) { e.clk.onclick = function () { e.Next(); return false; }; }
    e.prv = $C(e, 'prv', '', 0); e.nxt = $C(e, 'nxt', '', 0);
    if (e.nxt) { e.nxt.onclick = function () { e.Next(); return false; }; }
    if (e.prv) { e.prv.onclick = function () { e.Prev(); return false; }; }
    e.Start(1);
    return e;
};
var albPhoto = PhotoAlbum('AlbumPhotos');

