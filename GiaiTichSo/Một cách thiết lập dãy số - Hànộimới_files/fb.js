function SocialPlugin() {
    var t = this,
        e = null;
    this.isFBAvailable = !1, this.isFBLogin = !1, this.publish_permission = !1;
    var n = function (e) {
        jQuery.ajax({
            async: !0,
            type: "GET",
            url: "https://connect.facebook.net/vi_VN/all.js#xfbml=1&appId=" + APP_ID,
            dataType: "script",
            cache: !0,
            data: null,
            complete: function (n, i) {
                200 == n.status ? (t.isFBAvailable = !0, "function" == typeof e && e()) : "function" == typeof e && e("Facebook is not accessible!")
            }
        })
    };
    this.init = function () {
        "" != window.location.host && n(function (e) {
            e || (window.fbAsyncInit = function () {
                "undefined" != typeof FB && FB && (FB.init({
                    appId: APP_ID,
                    logging: !1,
                    status: !0,
                    cookie: !0
                }), $("body").addClass("fbonline"), FB.Event.subscribe("edge.create", function (e, n) {
                    e.search("http://hanoimoi.com.vn/share/link.aspx") >= 0 || ($(n).parents(".btnSocial").css("overflow", "visible"), t.showFanpagePopup())
                }), FB.Event.subscribe("auth.statusChange", i), FB.XFBML.parse())
            })
        })
    };
    var i = function (n, i) {
        if ("connected" === n.status) {
            var a = n.authResponse.userID,
                o = n.authResponse.accessToken;
            $("body").addClass("fbAuthorized"), FB.api("/" + a, function (n) {
                e = {
                    user_name: n.name && "" != n.name ? n.name : n.last_name + " " + n.first_name,
                    user_email: n.email ? n.email : n.username ? n.username + "@facebook.com" : n.link,
                    user_id: n.id,
                    user_avatar: "http://graph.facebook.com/" + n.id + "/picture?type=square"
                }, t.isFBLogin = !0, "function" == typeof i && i(null, e)
            }), FB.api("/" + a + "/permissions", function (e) {
                e.data && (t.publish_permission = _.findLastIndex(e.data, {
                    permission: "publish_actions",
                    status: "granted"
                }) >= 0, t.publish_permission)
            })
        } else "not_authorized" === n.status ? (t.isFBLogin = !0, "function" == typeof i && i("User login to FB but hasn't authorized Zing.vn")) : "function" == typeof i && i("User hasn't login to their FB account")
    };
    this.showFanpagePopup = function () {
        if (void 0 != FB) {
            if (null == t.userinfo || !t.isFBLogin) {
                var e = storage.loadContent("popup_follow");
                return void ((null == e || e === !1 || e.age > 1e4) && page.showFollowDialog())
            }
            FB.api({
                method: "fql.query",
                query: "SELECT uid FROM page_fan WHERE uid=" + t.userinfo.id + " AND page_id=1414411772114879"
            }, function (t) {
                var e = storage.loadContent("popup_follow");
                !t || t.error ? (null == e || e === !1 || e.age > 1e4) && page.showFollowDialog() : t.length || (null == e || e === !1 || e.age > 1e4) && page.showFollowDialog()
            })
        }
    }, this.login = function (t) {
        return e ? void ("function" == typeof t && t(null, e)) : void FB.login(function (e) {
            e.authResponse ? i(e, t) : "function" == typeof t && t("User cancelled login or did not fully authorize.")
        }, {
            scope: "publish_actions",
            return_scopes: !0
        })
    }, this.logout = function (t) {
        "undefined" != typeof FB && FB && (e = null, FB.getLoginStatus(function (e) {
            FB.logout(function (e) {
                "function" == typeof t && t()
            })
        }))
    }, this.shareComment = function (e, n, i) {
        return "undefined" != typeof FB && FB ? t.isFBLogin && t.publish_permission ? void FB.api("comment", "post", {
            article: n,
            message: e,
            "fb:explicitly_shared": !0
        }, function (t) {
            t && !t.error ? "function" == typeof i && i() : "function" == typeof i && i("Error sharing comment to Facebook")
        }) : void ("function" == typeof i && i("User hasn't no login/authorize permission for this action!")) : void ("function" == typeof i && i("Facebook is not accessible. Share cancel!"))
    }, this.share = function (t, e) {
        if ("undefined" == typeof FB || !FB) return void ("function" == typeof e && e("Facebook inaccessible or not initialized"));
        var n = {
            method: "share",
            href: t,
            display: "popup"
        };
        FB.ui(n, function (t) {
            "function" == typeof e && e()
        })
    }, this.like = function (t, e, n) {
        if (void 0 == typeof FB) return void (e && e(!1));
        var i = null,
            a = !0;
        n === !1 ? a = !1 : "" != n && (i = n), FB.api("me/og.likes", "post", {
            object: t,
            message: i,
            "fb:explicitly_shared": !1
        }, function (t) {
            if (t.error && 3501 == t.error.code || t.id) {
                var n;
                n = t.id ? t.id : t.error.message.match(/\d+$/i)[0], page.socialplugin.showFanpagePopup(), e(!0, n)
            } else e(!1)
        })
    }
}
var APP_ID = "481358161896725",
facebook = new SocialPlugin;
$(window).load(function () {
    facebook.init();
});