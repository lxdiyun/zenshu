jQuery ->
maybeScrollToHash()
	setTimeout (-> maybeScrollToHash()), 100

$(window).bind 'hashchange', ->
maybeScrollToHash()

	@maybeScrollToHash = ->
	if window.location.hash
	hash_name = window.location.hash.split('#')[1]
	section = $("a[name='#{hash_name}']")
	section = $("#"+hash_name) if section.length == 0

	if section.length
new_top = section.offset().top - $('.navbar').height()
$(window).scrollTop(new_top)
