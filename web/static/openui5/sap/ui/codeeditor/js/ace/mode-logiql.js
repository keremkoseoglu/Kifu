ace.define("ace/mode/logiql_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"],function(r,e,m){"use strict";var o=r("../lib/oop");var T=r("./text_highlight_rules").TextHighlightRules;var L=function(){this.$rules={start:[{token:'comment.block',regex:'/\\*',push:[{token:'comment.block',regex:'\\*/',next:'pop'},{defaultToken:'comment.block'}]},{token:'comment.single',regex:'//.*'},{token:'constant.numeric',regex:'\\d+(?:\\.\\d+)?(?:[eE][+-]?\\d+)?[fd]?'},{token:'string',regex:'"',push:[{token:'string',regex:'"',next:'pop'},{defaultToken:'string'}]},{token:'constant.language',regex:'\\b(true|false)\\b'},{token:'entity.name.type.logicblox',regex:'`[a-zA-Z_:]+(\\d|\\a)*\\b'},{token:'keyword.start',regex:'->',comment:'Constraint'},{token:'keyword.start',regex:'-->',comment:'Level 1 Constraint'},{token:'keyword.start',regex:'<-',comment:'Rule'},{token:'keyword.start',regex:'<--',comment:'Level 1 Rule'},{token:'keyword.end',regex:'\\.',comment:'Terminator'},{token:'keyword.other',regex:'!',comment:'Negation'},{token:'keyword.other',regex:',',comment:'Conjunction'},{token:'keyword.other',regex:';',comment:'Disjunction'},{token:'keyword.operator',regex:'<=|>=|!=|<|>',comment:'Equality'},{token:'keyword.other',regex:'@',comment:'Equality'},{token:'keyword.operator',regex:'\\+|-|\\*|/',comment:'Arithmetic operations'},{token:'keyword',regex:'::',comment:'Colon colon'},{token:'support.function',regex:'\\b(agg\\s*<<)',push:[{include:'$self'},{token:'support.function',regex:'>>',next:'pop'}]},{token:'storage.modifier',regex:'\\b(lang:[\\w:]*)'},{token:['storage.type','text'],regex:'(export|sealed|clauses|block|alias|alias_all)(\\s*\\()(?=`)'},{token:'entity.name',regex:'[a-zA-Z_][a-zA-Z_0-9:]*(@prev|@init|@final)?(?=(\\(|\\[))'},{token:'variable.parameter',regex:'([a-zA-Z][a-zA-Z_0-9]*|_)\\s*(?=(,|\\.|<-|->|\\)|\\]|=))'}]};this.normalizeRules();};o.inherits(L,T);e.LogiQLHighlightRules=L;});ace.define("ace/mode/folding/coffee",["require","exports","module","ace/lib/oop","ace/mode/folding/fold_mode","ace/range"],function(r,e,m){"use strict";var o=r("../../lib/oop");var B=r("./fold_mode").FoldMode;var R=r("../../range").Range;var F=e.FoldMode=function(){};o.inherits(F,B);(function(){this.getFoldWidgetRange=function(s,f,a){var b=this.indentationBlock(s,a);if(b)return b;var c=/\S/;var l=s.getLine(a);var d=l.search(c);if(d==-1||l[d]!="#")return;var g=l.length;var h=s.getLength();var i=a;var j=a;while(++a<h){l=s.getLine(a);var k=l.search(c);if(k==-1)continue;if(l[k]!="#")break;j=a;}if(j>i){var n=s.getLine(j).length;return new R(i,g,j,n);}};this.getFoldWidget=function(s,f,a){var l=s.getLine(a);var i=l.search(/\S/);var n=s.getLine(a+1);var p=s.getLine(a-1);var b=p.search(/\S/);var c=n.search(/\S/);if(i==-1){s.foldWidgets[a-1]=b!=-1&&b<c?"start":"";return"";}if(b==-1){if(i==c&&l[i]=="#"&&n[i]=="#"){s.foldWidgets[a-1]="";s.foldWidgets[a+1]="";return"start";}}else if(b==i&&l[i]=="#"&&p[i]=="#"){if(s.getLine(a-2).search(/\S/)==-1){s.foldWidgets[a-1]="start";s.foldWidgets[a+1]="";return"";}}if(b!=-1&&b<i)s.foldWidgets[a-1]="start";else s.foldWidgets[a-1]="";if(i<c)return"start";else return"";};}).call(F.prototype);});ace.define("ace/mode/matching_brace_outdent",["require","exports","module","ace/range"],function(r,e,m){"use strict";var R=r("../range").Range;var M=function(){};(function(){this.checkOutdent=function(l,i){if(!/^\s+$/.test(l))return false;return/^\s*\}/.test(i);};this.autoOutdent=function(d,a){var l=d.getLine(a);var b=l.match(/^(\s*\})/);if(!b)return 0;var c=b[1].length;var o=d.findMatchingBracket({row:a,column:c});if(!o||o.row==a)return 0;var i=this.$getIndent(d.getLine(o.row));d.replace(new R(a,0,a,c-1),i);};this.$getIndent=function(l){return l.match(/^\s*/)[0];};}).call(M.prototype);e.MatchingBraceOutdent=M;});ace.define("ace/mode/logiql",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/logiql_highlight_rules","ace/mode/folding/coffee","ace/token_iterator","ace/range","ace/mode/behaviour/cstyle","ace/mode/matching_brace_outdent"],function(r,e,m){"use strict";var o=r("../lib/oop");var T=r("./text").Mode;var L=r("./logiql_highlight_rules").LogiQLHighlightRules;var F=r("./folding/coffee").FoldMode;var a=r("../token_iterator").TokenIterator;var R=r("../range").Range;var C=r("./behaviour/cstyle").CstyleBehaviour;var M=r("./matching_brace_outdent").MatchingBraceOutdent;var b=function(){this.HighlightRules=L;this.foldingRules=new F();this.$outdent=new M();this.$behaviour=new C();};o.inherits(b,T);(function(){this.lineCommentStart="//";this.blockComment={start:"/*",end:"*/"};this.getNextLineIndent=function(s,l,t){var i=this.$getIndent(l);var c=this.getTokenizer().getLineTokens(l,s);var d=c.tokens;var f=c.state;if(/comment|string/.test(f))return i;if(d.length&&d[d.length-1].type=="comment.single")return i;var g=l.match();if(/(-->|<--|<-|->|{)\s*$/.test(l))i+=t;return i;};this.checkOutdent=function(s,l,i){if(this.$outdent.checkOutdent(l,i))return true;if(i!=="\n"&&i!=="\r\n")return false;if(!/^\s+/.test(l))return false;return true;};this.autoOutdent=function(s,d,c){if(this.$outdent.autoOutdent(d,c))return;var p=d.getLine(c);var f=p.match(/^\s+/);var g=p.lastIndexOf(".")+1;if(!f||!c||!g)return 0;var l=d.getLine(c+1);var h=this.getMatching(d,{row:c,column:g});if(!h||h.start.row==c)return 0;g=f[0].length;var i=this.$getIndent(d.getLine(h.start.row));d.replace(new R(c+1,0,c+1,g),i);};this.getMatching=function(s,c,d){if(c==undefined)c=s.selection.lead;if(typeof c=="object"){d=c.column;c=c.row;}var f=s.getTokenAt(c,d);var K="keyword.start",g="keyword.end";var t;if(!f)return;if(f.type==K){var i=new a(s,c,d);i.step=i.stepForward;}else if(f.type==g){var i=new a(s,c,d);i.step=i.stepBackward;}else return;while(t=i.step()){if(t.type==K||t.type==g)break;}if(!t||t.type==f.type)return;var h=i.getCurrentTokenColumn();var c=i.getCurrentTokenRow();return new R(c,h,c,h+t.value.length);};this.$id="ace/mode/logiql";}).call(b.prototype);e.Mode=b;});(function(){ace.require(["ace/mode/logiql"],function(m){if(typeof module=="object"&&typeof exports=="object"&&module){module.exports=m;}});})();
