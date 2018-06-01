Attentional Blink AND many-stream experiment implemented with [Psychopy](https://github.com/psychopy/psychopy), branched off from  [nStreams](https://github.com/alexholcombe/nStream).
============================
Licensing: MIT license, like CC-BY for code which means do whatever you want with it, with an attribution to the author.

This was created for Humby's honours thesis, so that she could run her first experiment with two or three simultaneous targets.


** NOTES **


### 2 cues 3 lineups

The wrong cues are getting drawn. It's always drawing the first two cues but when their positions were set it was assumed each one was streams 0,1,2.  Is it ok to only draw 0 and 1, in the positions of the streams that need cuing?

Updating drawResponseArrays with whichLineupEachResp and whichResp

### Randomisation of query order and which streams each cue

- For two targets, whichStreamEachCue = [2,0] but whichStreamEachResp[1]==1 when should be 0 presumably

- Now I'm randomising the query order by, at trialHandler, randoming whichStreamEachCue, which simultaneously decides which streams are cued. So, whichStreamEachResp should just inherit whichStreamEachCue I guess

- whichStreamEachResp, whichStreamEachCue, whichRespEachCue

-columns out of whack, check out whether correct0 is meant to be letter or number

- What's happening with counterbalancing of which stream respond to first in 3-target case? line 735

- Alex work on handleAndScoreResponse for 2 cues but 3 streams, hence pay attention to whichStreamEachCue
Needs to be out of 6 to counterbalance both 3 and 2-target conditions

	- Seems like whichstreamEachCue taking the place of whichCued. But I do need to counterbalance whichCued. So, maybe use which Cude only in trialHandler loop	
-Also need to handle eyetracking


### Jen ###

* check it's really getting randomised
* check program's variation in serial position of targets, eg Kim's latest paper uses 5->12





### Random notes ###

- Only working now for 3 streams, lot of vestigial nonworking code for fewer/more streams

- whichStreamEachResp (and also whichRespEachCue) is set up by doRSVPstim
