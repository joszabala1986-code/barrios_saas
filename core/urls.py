from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [

    # 🟢 HOME → LOGIN
    path('', views.login_view, name='home'),

    # 🔐 LOGIN / LOGOUT
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 👤 USUARIO
    path('mis-deudas/', views.mis_deudas, name='mis_deudas'),
    path('subir-comprobante/<int:deuda_id>/', views.subir_comprobante, name='subir_comprobante'),
    path('descargar-comprobantes/', views.descargar_comprobantes, name='descargar_comprobantes'),
    path('ver-contrato/', views.ver_contrato, name='ver_contrato'),

    # 🧑‍💼 ADMIN (tu dashboard, NO django admin)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pagos-pendientes/', views.pagos_pendientes, name='pagos_pendientes'),
    path('aprobar-pago/<int:pago_id>/', views.aprobar_pago, name='aprobar_pago'),
    path('rechazar-pago/<int:pago_id>/', views.rechazar_pago, name='rechazar_pago'),
    path('morosos/', views.morosos, name='morosos'),
    path('morosos/exportar/', views.exportar_morosos_excel, name='exportar_morosos'),

    # 🏘 LOTES Y DEUDAS
    path('lotes/', views.lotes_barrio, name='lotes'),
    path('crear-deuda/<int:lote_id>/', views.crear_deuda_lote, name='crear_deuda_lote'),
    path('generar-deuda/', views.generar_deuda_masiva, name='generar_deuda'),
    path('lote/<int:lote_id>/', views.ficha_lote, name='ficha_lote'),
    path('eliminar-deuda/<int:deuda_id>/', views.eliminar_deuda, name='eliminar_deuda'),
    path('pago-efectivo/<int:deuda_id>/', views.pago_efectivo, name='pago_efectivo'),

    # 👥 PROPIETARIOS
    path('crear-propietario/', views.crear_propietario, name='crear_propietario'),
    path('cambiar-propietario/<int:lote_id>/', views.cambiar_propietario, name='cambiar_propietario'),

    # 📊 HISTORIAL
    path('exportar-historial/', views.exportar_historial_lotes, name='exportar_historial'),
    path('historial-deudas/', views.exportar_historial_propietario, name='historial_deudas'),

    # 📢 COMUNICADOS
    path('crear-comunicado/', views.crear_comunicado, name='crear_comunicado'),

    # 🧾 FACTURAS
    path('facturas/', views.facturas, name='facturas'),
    path('guardar_factura/', views.guardar_factura, name='guardar_factura'),
    path('editar_factura/<int:factura_id>/', views.editar_factura, name='editar_factura'),
    path('eliminar_factura/<int:factura_id>/', views.eliminar_factura, name='eliminar_factura'),

    # 🧠 PANEL GENERAL
    path('panel-planta/', views.panel_planta, name='panel_planta'),

    # 🔐 CAMBIO DE CONTRASEÑA
    path('cambiar-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='password_change.html',
            success_url='/dashboard/'
        ),
        name='password_change'
    ),

    # 🔐 RESET PASSWORD
    path('password-reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'
    ),
    path('password-reset-done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path('reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),

    # 🧑‍💻 SUPERADMIN
    path('superadmin/', views.panel_superadmin, name='panel_superadmin'),
    path('crear-barrio/', views.crear_barrio, name='crear_barrio'),
    path('eliminar-barrio/<int:barrio_id>/', views.eliminar_barrio, name='eliminar_barrio'),
    path('editar-barrio/<int:barrio_id>/', views.editar_barrio, name='editar_barrio'),
    path('exportar-barrio/', views.exportar_barrio_excel, name='exportar_barrio'),

    # 📄 CONTRATO
    path('subir-contrato/', views.subir_contrato, name='subir_contrato'),

    # 💰 PAGOS
    path('marcar-pagado/<int:barrio_id>/', views.marcar_pagado, name='marcar_pagado'),

    # 🔐 SEGURIDAD
    path('seguridad/<int:barrio_id>/', views.panel_seguridad, name='panel_seguridad'),
    path('seguridad/<int:barrio_id>/crear/', views.crear_seguridad, name='crear_seguridad'),

    # LOGIN SEGURIDAD
    path('seguridad/login/', views.login_seguridad, name='login_seguridad'),
    path('seguridad/logout/', views.logout_seguridad, name='logout_seguridad'),

    # PANEL GUARDIA
    path('seguridad/panel/', views.panel_guardia, name='panel_guardia'),

    # INGRESO / EGRESO
    path('seguridad/ingreso/', views.registrar_movimiento, {'tipo': 'ingreso'}, name='registrar_ingreso'),
    path('seguridad/egreso/', views.registrar_movimiento, {'tipo': 'egreso'}, name='registrar_egreso'),

    # CRUD SEGURIDAD
    path('seguridad/eliminar/<int:seguridad_id>/', views.eliminar_seguridad, name='eliminar_seguridad'),
    path('seguridad/editar/<int:seguridad_id>/', views.editar_seguridad, name='editar_seguridad'),

    # EXPORTAR
    path('exportar-excel/<int:barrio_id>/', views.exportar_excel, name='exportar_excel'),
    
    path('pago-adelantado/', views.pago_adelantado, name='pago_adelantado'),
    
    # OFFLINE
    path('offline/', views.offline_view, name='offline'),
    
]


