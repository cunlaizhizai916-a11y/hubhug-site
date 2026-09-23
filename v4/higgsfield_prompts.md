# v4 用 Higgsfield 生成プロンプト（8枚・すべて 16:9・2048px以上）

共通の末尾：photorealistic, cinematic, 35mm, natural light, no text, no logo, no people's faces recognizable, Japanese urban setting, muted navy-and-warm-amber palette

| ファイル名 | シーン | プロンプト |
|---|---|---|
| cover.jpg | 表紙 | A narrow Osaka side street at blue hour, one small restaurant with its lights on among shuttered shops, wet pavement reflecting amber light, wide shot |
| morning.jpg | 06:00 | Interior of a small Japanese izakaya at dawn, chairs still up, a single person setting up a coffee stand on the counter, soft window light |
| daytime.jpg | 11:00 | The same counter at noon, lunch service, steam from a pot, three customers seen from behind, warm daylight |
| evening.jpg | 17:00 | The same space at dusk, lights being switched on for evening service, hands wiping the counter, amber and navy |
| close.jpg | 23:00 | Exterior of the same restaurant at night, shutter half down, street empty, one light still on inside |
| scheme.jpg | 契約 | Overhead shot of a wooden table with a lease contract, a building key, and two cups of tea, hands of two people at the edges, top-down |
| numbers.jpg | 収支 | Close-up of a handwritten ledger notebook on a restaurant counter, calculator, receipts, shallow depth of field |
| company.jpg | 会社 | Osaka cityscape from a low rooftop at dusk, dense small buildings, restaurant signs starting to light up |

差し替え：`v4/index.html` 内の `data-img="xxx"` を持つ要素の `background-image` を `../assets/img/v4/xxx.jpg` に変える。
