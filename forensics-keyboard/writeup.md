We're given a pcapng and its name is keyboard, so it's probably keyboard input. We can extract the keystrokes by running

`tshark -r keyboard.pcapng -T fields -e usb.capdata > keystrokes.txt`
`cat keystrokes.txt | awk 'NF' > pipe; cat pipe > keystrokes.txt`

which gives us keystrokes.txt. However, if we try converting this to text it looks like gibberish!

If you take note of how there are often multiple keystrokes at once, that should be a clue that I'm treating this like a chorded keyboard. If we check wikipedia for more information on keyboards/chorded keyboards, we'll eventually come across stenotype, which is what court reporters use. If we search for "stenotype keyboard" or "stenography keyboard", we'll get some results for specialized keyboards which probably aren't what we're looking for. In the pcapng we can find the keyboard model, which is a Razer Huntsman V2 Tenkeyless keyboard which is a pretty normal keyboard. Searching for "stenography on normal keyboard", we'll find a bunch of resources, most of which recommends using Plover for steno software. And if we visit Plover, we'll be greeted with
> Plover (rhymes with "lover")

So this is definitely what we're looking for! Now we just need to group the output into chords and convert it to the stenotype keys so that we can look the words up in Plover's dictionary. Easier said than done so maybe there's an easier way. My solve script is kind of jank and you have to remove some garbage. I think a better solution is to emulate my input and feed it through plover or their online demo.

I group the keystrokes together and then convert them to the stenography chords, then look them up in the dictionary. It's not perfect. My script only recovers this:
`set flag to ut flag { learning _ snog if I stenography_ on _ a _ convert {^y} qwerty_ keyboard _ is _  quite _ difficult } and the make sure to {re^} move any spay`

So although all parts of the flag are there, it's not a clean solution. But I made the flag a grammatically correct sentence to make it easier for people to spot errors.

Common Questions:

Sanity check on the keyboard output? If it starts with wcsf⌫ or ends with ⌫aw you're missing characters. Full output can be seen in keys.txt (I replaced del with @ for visibility).

Asking about keyboard layouts? Well yes, its a different layout but that knowledge won't help you. You need to figure out what I'm doing to get the layout.

Mention steno/chording? You're on the right track.

First or last 2 words are wrong? Some chords are longer than 5/6 keystrokes. Do you properly handle these?

