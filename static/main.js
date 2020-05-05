"use strict";
var accessToken = null;
var curUserID = null;
var curPlaylist = null;
var is_playing = false;
var audio = $("<audio>");
var songTable;

function error(msg) {
    info(msg);
}

function info(msg) {
    $("#info").text(msg);
}

function authorizeUser() {
    var scopes = 'user-library-read playlist-read-private playlist-read-collaborative user-modify-playback-state user-read-cur' +
        ' user-read-playback-state app-remote-control user-library-read playlist-modify-public';

    var url = 'https://accounts.spotify.com/authorize?client_id=' + SPOTIFY_CLIENT_ID +
        '&response_type=token' +
        '&scope=' + encodeURIComponent(scopes) +
        '&redirect_uri=' + encodeURIComponent(SPOTIFY_REDIRECT_URI);
    document.location = url;
}
function parseArgs() {
    var hash = location.hash.replace(/#/g, '');
    var all = hash.split('&');
    var args = {};
    _.each(all, function(keyvalue) {
        var kv = keyvalue.split('=');
        var key = kv[0];
        var val = kv[1];
        args[key] = val;
    });
    return args;
}


function getSpotify(url, data, callback) {
    $.ajax(url, {
        dataType: 'json',
        data: data,
        headers: {
            'Authorization': 'Bearer ' + accessToken
        },
        success: function(r) {
            callback(r);
        },
        error: function(r) {
            callback(null);
        }
    });
}

function showPlaylists() {
    $(".worker").hide();
    $("#playlists").show();
}

function fetchSinglePlaylist(playlist) {
    $(".worker").hide();
    $("#single-playlist").show();
    $("#single-playlist-contents").hide();
    $(".spinner2").show();
    $("#song-table tbody").empty();
    window.scrollTo(0,0);
    songTable.clear();
    $("#playlist-title").text(playlist['name']);
    $("#playlist-title").attr('value', playlist['uri']);
    $(".spinner2").hide();
    curPlaylist = playlist['uri'];
    $.ajax({
        headers :{
            username: curUserID,
            token: accessToken
        },
        data: { playlist_uri: playlist['uri'] },
        type : 'PUT',
        url : '/set-playlist',
    });
    $("#single-playlist-contents").show();
}

function fetchPlaylists(uid, callback) {
    $("#playlist-list tbody").empty();
    $(".prompt").hide();
    $(".spinner").show();
    info("Getting your playlists");
    $.ajax({
        headers :{
            username: curUserID,
            token: accessToken
        },
        type : 'GET',
        url : '/playlists',
        success: function (data) {
            playlistLoaded(data.playlists)
        }
    });

}

function fetchCurrentUserProfile(callback) {
    var url = 'https://api.spotify.com/v1/me';
    getSpotify(url, null, callback);
}

function playlistLoaded(playlists) {
    var pl = $("#playlist-list tbody");
    $(".prompt").show();
    $(".spinner").hide();
    if (playlists) {
        info("");
        _.each(playlists, function(playlist) {
            var tr = $("<tr>");

            var tdName = $("<td>")

            var aName = $("<a>")
                .text(playlist['name'])
                .addClass('hoverable')
                .on('click', function() {
                    fetchSinglePlaylist(playlist);
                });
            tdName.append(aName);
            var tdTrackCount = $("<td>").text(playlist["tracks"]);
            var tdOwner = $("<td>").text(playlist["owner"]);
            tr.append(tdName);
            tr.append(tdTrackCount);
            tr.append(tdOwner);
            pl.append(tr);
        });
        if (playlists.next) {
            getSpotify(playlists.next, null, playlistLoaded);
        }
    } else {
        error("Sorry, I couldn't find your playlists");
    }
}

function loadPlaylists(uid) {
    $("#playlists").show();
    fetchPlaylists(uid, playlistLoaded);
}

function initTable() {
    var table = $("#song-table").DataTable( {
            paging: false,
            searching: true,  // searching must be enabled for filtering to work
            info:false,
            dom:"t", // only show table (exclude search bar)
            columnDefs: [
                { type : "time-uni", targets:9},
            ]
     });

    $("#song-table tbody").on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
            var row = songTable.row( $(this) );
            stopTrack();
        } else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
            var row = songTable.row( $(this) );
            var rowData = row.data();
            var track = rowData[rowData.length - 1];
            playTrack(track);
        }
    } );
    return table;
}

$(document).ready(
    function() {
        songTable = initTable();
        var args = parseArgs();
        if ('error' in args) {
            error("Sorry, I can't read your playlists from Spotify without authorization");
            $("#go").show();
            $("#go").on('click', function() {
                authorizeUser();
                get_Playlists();
            });
        } else if ('access_token' in args) {
            accessToken = args['access_token'];
            $(".worker").hide();
            fetchCurrentUserProfile(function(user) {
                if (user) {
                    curUserID = user.id;
                    $("#who").text(user.id);
                    loadPlaylists(user.id);
                } else {
                    error("Trouble getting the user profile");
                }
            });
        } else {
            $("#go").show();
            $("#go").on('click', function() {
                authorizeUser();
                get_Playlists();
            });
        }
        $("#pick").on('click', function() {
            showPlaylists();
        });
        $("#play-pause").on('click', function () {
            $.ajax({
                headers: {
                    username: curUserID,
                    token: accessToken
                },
                type: 'PUT',
                url: is_playing? '/pause' : '/play',
                success: function () {
                    is_playing = !is_playing
                },
            });
        });
        $("#skip").on('click', function () {
            $.ajax({
                headers: {
                    username: curUserID,
                    token: accessToken
                },
                type: 'PUT',
                url: '/skip',
            });
        });
        $('#min-bpm,#max-bpm,#include-double').on('keyup change', function() {
            songTable.draw();
        });
    }
);