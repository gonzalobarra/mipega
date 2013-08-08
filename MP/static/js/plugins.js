// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function f(){ log.history = log.history || []; log.history.push(arguments); if(this.console) { var args = arguments, newarr; args.callee = args.callee.caller; newarr = [].slice.call(args); if (typeof console.log === 'object') log.apply.call(console.log, console, newarr); else console.log.apply(console, newarr);}};

// make it safe to use console.log always
(function(a){function b(){}for(var c="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,markTimeline,profile,profileEnd,time,timeEnd,trace,warn".split(","),d;!!(d=c.pop());){a[d]=a[d]||b;}})
(function(){try{console.log();return window.console;}catch(a){return (window.console={});}}());

/**
 * Ajax with django
 * https://docs.djangoproject.com/en/1.4/ref/contrib/csrf/#ajax
 */
jQuery(document).ajaxSend(function(i,f,d){function g(a){var b=null;if(document.cookie&&""!=document.cookie)for(var c=document.cookie.split(";"),e=0;e<c.length;e++){var d=jQuery.trim(c[e]);if(d.substring(0,a.length+1)==a+"="){b=decodeURIComponent(d.substring(a.length+1));break}}return b}function h(a){var b="//"+document.location.host,c=document.location.protocol+b;return a==c||a.slice(0,c.length+1)==c+"/"||a==b||a.slice(0,b.length+1)==b+"/"||!/^(\/\/|http:|https:).*/.test(a)}!/^(GET|HEAD|OPTIONS|TRACE)$/.test(d.type)&&
h(d.url)&&f.setRequestHeader("X-CSRFToken",g("csrftoken"))});