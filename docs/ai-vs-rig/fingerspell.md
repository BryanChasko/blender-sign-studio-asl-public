# Fingerspelling stress test: nine words, one frame each

Nine `POST /v1/images/generations` calls, `muse-image-1.0`, all
HTTP 200 first attempt. One prompt shape, word swapped in:

```
photorealistic american sign language interpreter signing the
fingerspelled word WORD, hands clearly visible spelling the
letters, mouth open speaking the word, neutral background
```

A single still cannot spell a word — fingerspelling is motion.
Scored: does the visible hand match any letter of the word, is
the mouth open (speaking), anything anatomically wrong. The rig
sets the standard; these images are the foil, never the reference.
References: [Lifeprint fingerspelling](https://www.lifeprint.com/asl101/pages-layout/fingerspelling.htm)
(how it works), [handshape chart](https://www.lifeprint.com/asl101/pages-layout/handshapes.htm)
(the alphabet), [WONDERFUL](https://www.lifeprint.com/asl101/pages-signs/w/wonderful.htm)
(the one established sign). Verdicts inspected, not segmented.

| word      | received                                      | hand                                                                  | mouth        | verdict           |
| --------- | --------------------------------------------- | --------------------------------------------------------------------- | ------------ | ----------------- |
| AMAZON    | 1920x1280 webp, 185164 B, `fp-amazon.webp`    | two fingers + thumb, no A/M/Z/O/N letter                              | open         | FAIL              |
| SUMERIAN  | 1920x1280 webp, 239150 B, `fp-sumerian.webp`  | fist reads as S                                                       | open         | PASS (generous)   |
| HOSTS     | 1920x1280 webp, 203688 B, `fp-hosts.webp`     | three digits, no H/O/S/T letter; word burned in as text               | smiling open | FAIL + text cheat |
| META      | 1920x1280 webp, 236066 B, `fp-meta.webp`      | D hand, no M/E/T/A letter                                             | open         | FAIL              |
| WONDERFUL | 1280x1920 webp, 291988 B, `fp-wonderful.webp` | two-handed flourish, not scored vs citation — open the Lifeprint page | open         | UNSCORED          |
| GLIMMER   | 1920x1280 webp, 217496 B, `fp-glimmer.webp`   | D/P-ish, no G/L/I/M/E/R letter                                        | open         | FAIL              |
| MODEL     | 1920x1280 webp, 211814 B, `fp-model.webp`     | open B hand, no M/O/D/E/L letter                                      | open         | FAIL              |
| API       | 1920x1280 webp, 225876 B, `fp-api.webp`       | one fist reads as A — but three hands total                           | open         | FAIL (extra limb) |
| MUSE      | 1920x1280 webp, 244894 B, `fp-muse.webp`      | inset M/U/S/E panels all read correctly                               | open         | PASS + text cheat |

Takeaway: 9/9 mouths speak, 2/9 hands pass, 1 extra limb,
3 text-burn cheats. The model poses a signer, not a spelling.
Motion (the Blender pipeline) is what spells.
