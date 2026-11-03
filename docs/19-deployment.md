# 游格部署与后续更新

## 已选方案

- GitHub：`niziyu0430-ux/youge`，公开仓库，主分支 `main`。
- 网站运行：Render Python Web Service，免费验证方案；域名最终使用 `life-counter.cn`，替换原人生计算器。
- 后端入口：`gunicorn --config gunicorn.conf.py 'youge.production:create_app()'`。
- 构建命令：`pip install -r requirements.txt`。
- 健康检查：`/api/health`。
- 密码：在托管平台设置秘密环境变量 `YOUGE_ACCESS_PASSWORD`。本地 `.local/` 与任何 `.env` 均不入库，文档不记录正式密码。

`render.yaml` 可创建同样配置。没有秘密环境变量时，正式入口拒绝启动，不生成任何可猜测的默认密码。

## 保留的功能

正式入口复用原有路由、认证、题包、计分和报告生成程序。登录状态仍只在当前网页文档内存中；刷新重新登录，同一页面内可不限次数测试。答卷与档案继续保存在访客自己的浏览器，不上传形成用户数据库。

当前会话放在一个服务进程内，因此 `gunicorn.conf.py` 固定一个工作进程、8个线程。部署、重启或免费服务休眠会使现有登录失效，重新输入密码即可继续。扩容多实例前需把会话及限流状态迁移至共享存储，不能直接增加进程或实例数。

Render 前方有平台代理；首轮保守地按实际连接来源限流，不信任客户端随意传入的转发头。生产访问量增加前，应按平台确认的可信代理规则配置真实来源识别。

## 域名切换顺序

1. 先部署并验收 Render 返回的实际临时网址，检查密码、取题、完成测试、报告和刷新。
2. 在该服务的 Custom Domains 添加 `life-counter.cn`，读取平台给出的 DNS 要求。
3. 在腾讯云 DNSPod 记录现有主机记录、类型、值和 TTL，保存回退信息。
4. 仅按 Render 此次返回的要求调整根域名与 `www` 的网站解析，保留邮件等无关记录。
5. 验证域名与自动 HTTPS 证书后，再检查公网访问。只有域名实际返回游格，才算切换完成。

初次检查时，根域名网站指向 GitHub Pages（A记录 `185.199.108.153`），DNSPod名称服务器为 `coral.dnspod.net` 与 `cloth.dnspod.net`。这些是2026-11-03的观察记录，回退前应以实际保存的完整记录为准。人生计算器原仓库保留，便于回退。

## 后续题库与网页同步

在本项目内继续编辑。已配置的 GitHub Actions 会检查认证、HTTP路由、生产入口与核心报告兼容性。

```powershell
python -m unittest tests.test_access tests.test_web tests.test_v04 tests.test_production
git status --short
git add config web youge docs scripts tests exports README.md
git diff --cached --stat
git commit -m "Update authored game questionnaires"
git push origin main
```

上传新题包时同时保留 `config/question-packs-history/` 和当前题库索引，避免旧答卷失去兼容性。首次部署若用公开仓库URL且尚未连接Git提供商，可先在Render中使用 Manual Deploy → Deploy latest commit；连接GitHub提供商后再启用主分支自动部署。连接前应由账号拥有者确认授权范围。域名只需首次配置，之后更新题库不用重复修改DNS。

免费方案适合本阶段验证；闲置15分钟会休眠，下一位访问者可能需等待约一分钟。正式收费运营前应改用常驻实例，并验证实际访问地区的可用性。

## youge.cn 与网站名称

网站名称可以始终显示“游格”，与域名不同不影响功能。若拥有 `youge.cn`，可以将它添加为自定义域名，或配置HTTPS重定向到 `life-counter.cn`；未拥有该域名时，无法控制它的访问去向。未购买新域名时也可以使用 `youge.life-counter.cn`，它属于现有域名的子域名。搜索引擎搜索“游格”能否找到网站，则另取决于公开页面和收录；域名跳转不等于搜索收录。

## 官方参考

- [GitHub Pages 是静态托管](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)
- [Render 免费实例说明](https://render.com/docs/free)
- [Render Python与Gunicorn部署](https://render.com/docs/deploy-flask)
- [Render 自定义域名及HTTPS](https://render.com/docs/custom-domains)
