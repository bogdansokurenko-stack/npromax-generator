<?php
/* NPROMAX lead intake (оренда / B2B / 1-клік / консультація).
   POST JSON -> leads table -> email -> Telegram (якщо налаштовано). Returns {ok, lead_no}.
   Мета: заявка з платного трафіку не залежить від одного email-каналу. */
require dirname(__DIR__) . '/_shopcore.php';
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
  http_response_code(405); echo json_encode(['ok' => false, 'error' => 'method']); exit;
}

$raw = file_get_contents('php://input');
$d = json_decode($raw, true);
if (!is_array($d)) { $d = $_POST; }

// honeypot: вдаємо успіх, нічого не зберігаємо
if (!empty($d['_honey'])) { echo json_encode(['ok' => true, 'lead_no' => '']); exit; }

$cut = function ($v, $n) { return mb_substr(trim((string)$v), 0, $n); };
$phone = $cut($d['phone'] ?? '', 40);
if ($phone === '') { http_response_code(422); echo json_encode(['ok' => false, 'error' => 'validation']); exit; }

$type = $cut($d['type'] ?? 'lead', 32);          // rental | b2b | one_click | consult
$row = [
  'type'    => $type,
  'name'    => $cut($d['name'] ?? '', 120),
  'phone'   => $phone,
  'email'   => $cut($d['email'] ?? '', 120),
  'city'    => $cut($d['city'] ?? '', 120),
  'place'   => $cut($d['place'] ?? '', 120),
  'color'   => $cut($d['color'] ?? '', 40),
  'cups'    => $cut($d['cups'] ?? '', 40),
  'product' => $cut(($d['product'] ?? $d['service'] ?? ''), 190),
  'comment' => $cut($d['comment'] ?? '', 1000),
  'utm_source'   => $cut($d['utm_source'] ?? '', 120),
  'utm_medium'   => $cut($d['utm_medium'] ?? '', 120),
  'utm_campaign' => $cut($d['utm_campaign'] ?? '', 190),
  'utm_content'  => $cut($d['utm_content'] ?? '', 190),
  'utm_term'     => $cut($d['utm_term'] ?? '', 190),
  'fbclid'  => $cut($d['fbclid'] ?? '', 255),
  'gclid'   => $cut(($d['gclid'] ?? $d['wbraid'] ?? $d['gbraid'] ?? ''), 255),
  'page'    => $cut($d['page'] ?? '', 255),
  'ip'      => substr((string)($_SERVER['REMOTE_ADDR'] ?? ''), 0, 45),
  'ua'      => $cut($_SERVER['HTTP_USER_AGENT'] ?? '', 255),
];

$lead_no = '';
$db_ok = false;
try {
  $pdo = shop_db();
  $pdo->exec("CREATE TABLE IF NOT EXISTS leads (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    lead_no VARCHAR(32) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    type VARCHAR(32) NOT NULL DEFAULT 'lead',
    name VARCHAR(120) NOT NULL DEFAULT '',
    phone VARCHAR(40) NOT NULL DEFAULT '',
    email VARCHAR(120) NOT NULL DEFAULT '',
    city VARCHAR(120) NOT NULL DEFAULT '',
    place VARCHAR(120) NOT NULL DEFAULT '',
    color VARCHAR(40) NOT NULL DEFAULT '',
    cups VARCHAR(40) NOT NULL DEFAULT '',
    product VARCHAR(190) NOT NULL DEFAULT '',
    comment TEXT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'new',
    utm_source VARCHAR(120) NOT NULL DEFAULT '',
    utm_medium VARCHAR(120) NOT NULL DEFAULT '',
    utm_campaign VARCHAR(190) NOT NULL DEFAULT '',
    utm_content VARCHAR(190) NOT NULL DEFAULT '',
    utm_term VARCHAR(190) NOT NULL DEFAULT '',
    fbclid VARCHAR(255) NOT NULL DEFAULT '',
    gclid VARCHAR(255) NOT NULL DEFAULT '',
    page VARCHAR(255) NOT NULL DEFAULT '',
    ip VARCHAR(45) NOT NULL DEFAULT '',
    ua VARCHAR(255) NOT NULL DEFAULT '',
    admin_note TEXT NULL,
    INDEX idx_status (status),
    INDEX idx_created (created_at),
    INDEX idx_type (type)
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci");

  $st = $pdo->prepare("INSERT INTO leads
    (lead_no, created_at, type, name, phone, email, city, place, color, cups, product, comment, status,
     utm_source, utm_medium, utm_campaign, utm_content, utm_term, fbclid, gclid, page, ip, ua)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,'new',?,?,?,?,?,?,?,?,?,?)");
  for ($try = 0; $try < 6; $try++) {
    $lead_no = 'LD-' . date('Ymd') . '-' . str_pad((string) random_int(0, 9999), 4, '0', STR_PAD_LEFT);
    try {
      $st->execute([
        $lead_no, date('Y-m-d H:i:s'), $row['type'], $row['name'], $row['phone'], $row['email'],
        $row['city'], $row['place'], $row['color'], $row['cups'], $row['product'], $row['comment'],
        $row['utm_source'], $row['utm_medium'], $row['utm_campaign'], $row['utm_content'], $row['utm_term'],
        $row['fbclid'], $row['gclid'], $row['page'], $row['ip'], $row['ua'],
      ]);
      $db_ok = true;
      break;
    } catch (PDOException $e) {
      if ($e->getCode() === '23000' && $try < 5) { continue; }
      throw $e;
    }
  }
} catch (Throwable $e) {
  // БД недоступна — не втрачаємо лід: далі йдуть email і Telegram
  $db_ok = false;
}

$TYPES = ['rental' => 'Оренда кавомашини', 'b2b' => 'Заявка для бізнесу',
          'one_click' => 'Купівля в 1 клік', 'consult' => 'Консультація'];
$title = $TYPES[$row['type']] ?? 'Заявка з сайту';

$txt = "{$title}" . ($lead_no ? " {$lead_no}" : '') . "\n"
  . 'Дата: ' . date('Y-m-d H:i') . "\n"
  . "Імʼя: {$row['name']}\nТелефон: {$row['phone']}\n"
  . ($row['email'] ? "Email: {$row['email']}\n" : '')
  . ($row['city'] ? "Місто: {$row['city']}\n" : '')
  . ($row['place'] ? "Тип: {$row['place']}\n" : '')
  . ($row['color'] ? "Колір: {$row['color']}\n" : '')
  . ($row['cups'] ? "Чашок/день: {$row['cups']}\n" : '')
  . ($row['product'] ? "Товар/послуга: {$row['product']}\n" : '')
  . ($row['comment'] ? "Коментар: {$row['comment']}\n" : '')
  . 'Джерело: ' . ($row['utm_source'] ?: '—') . ' / ' . ($row['utm_medium'] ?: '—')
  . ($row['utm_campaign'] ? ' / ' . $row['utm_campaign'] : '') . "\n"
  . ($row['gclid'] ? "gclid: {$row['gclid']}\n" : '')
  . ($row['fbclid'] ? "fbclid: {$row['fbclid']}\n" : '')
  . ($row['page'] ? "Сторінка: {$row['page']}\n" : '')
  . ($db_ok ? '' : "\n[!] БД недоступна — заявка лише в цьому листі\n");

// 1) email менеджеру
@mail('info@npromax.com.ua', "{$title}" . ($lead_no ? " {$lead_no}" : '') . ' — npromax.com.ua', $txt,
  "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=utf-8\r\nFrom: site@npromax.com.ua");

// 2) Telegram (працює, якщо у npromax_secret.php задані tg_token і tg_chat)
try {
  $cfg = shop_config();
  $tok = $cfg['tg_token'] ?? '';
  $chat = $cfg['tg_chat'] ?? '';
  if ($tok && $chat && function_exists('curl_init')) {
    $ch = curl_init("https://api.telegram.org/bot{$tok}/sendMessage");
    curl_setopt_array($ch, [
      CURLOPT_POST => true,
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_TIMEOUT => 6,
      CURLOPT_POSTFIELDS => http_build_query([
        'chat_id' => $chat,
        'text' => "🔔 {$txt}",
        'disable_web_page_preview' => true,
      ]),
    ]);
    curl_exec($ch);
    curl_close($ch);
  }
} catch (Throwable $e) { /* тихо: канал резервний */ }

echo json_encode(['ok' => true, 'lead_no' => $lead_no, 'stored' => $db_ok]);
