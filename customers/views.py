import csv
import pandas as pd
from datetime import date, timedelta
from io import BytesIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Purchase


from .models import Client, DocumentType
from .serializers import ClientSerializer


class ClientSearchView(APIView):

    def get(self, request):
        """
        /api/client/search/?document_type=CC&document_number=123456789
        """
        doc_type_code = request.query_params.get('document_type')
        document_number = request.query_params.get('document_number')

        if not doc_type_code or not document_number:
            return Response(
                {"detail": "Parámetros requeridos: document_type y document_number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doc_type = DocumentType.objects.get(code=doc_type_code)
        except DocumentType.DoesNotExist:
            return Response(
                {"detail": "Tipo de documento no válido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = Client.objects.prefetch_related('purchases').get(
                document_type=doc_type,
                document_number=document_number
            )
        except Client.DoesNotExist:
            return Response(
                {"detail": "Cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ClientSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    
class ClientExportView(APIView):
    """
    Exporta la información de un cliente (y opcionalmente sus compras) en CSV.
    GET /api/client/export/?document_type=CC&document_number=123456789
    """

    def get(self, request):
        doc_type_code = request.query_params.get('document_type')
        document_number = request.query_params.get('document_number')

        if not doc_type_code or not document_number:
            return Response(
                {"detail": "Parámetros requeridos: document_type y document_number"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doc_type = DocumentType.objects.get(code=doc_type_code)
        except DocumentType.DoesNotExist:
            return Response(
                {"detail": "Tipo de documento no válido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = Client.objects.prefetch_related('purchases').get(
                document_type=doc_type,
                document_number=document_number
            )
        except Client.DoesNotExist:
            return Response(
                {"detail": "Cliente no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Crear respuesta HTTP como archivo CSV
        filename = f"cliente_{doc_type.code}_{client.document_number}.csv"

        response = HttpResponse(
            content_type='text/csv; charset=utf-8'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        writer = csv.writer(response, delimiter=';')

        # Primera sección: datos del cliente
        writer.writerow(['Datos del cliente'])
        writer.writerow([
            'Tipo documento',
            'Número de documento',
            'Nombre',
            'Apellido',
            'Correo',
            'Teléfono'
        ])
        writer.writerow([
            client.document_type.code,
            client.document_number,
            client.first_name,
            client.last_name,
            client.email,
            client.phone
        ])

        writer.writerow([])  # Línea en blanco

        # Segunda sección: compras
        writer.writerow(['Compras del cliente'])
        writer.writerow([
            'Fecha de compra',
            'Monto',
            'Descripción',
            'Número de orden'
        ])

        for p in client.purchases.all():
            writer.writerow([
                p.purchase_date.isoformat(),
                float(p.amount),
                p.description or '',
                p.order_number or ''
            ])

        return response


class LoyalCustomersReportView(APIView):
    """
    Genera un reporte en Excel con los clientes que superan 5'000.000 COP
    en compras durante el último mes (últimos 30 días).
    GET /api/reports/loyal-customers/
    """

    def get(self, request):
        today = date.today()
        start_date = today - timedelta(days=30)

        # Traemos compras del último mes con el cliente y tipo de documento
        purchases = Purchase.objects.filter(
            purchase_date__gte=start_date
        ).select_related('client', 'client__document_type')

        if not purchases.exists():
            return Response(
                {"detail": "No hay compras registradas en el último mes."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Convertimos a una lista de dicts para meterlo a pandas
        rows = []
        for p in purchases:
            rows.append({
                'client_id': p.client.id,
                'document_type': p.client.document_type.code,
                'document_number': p.client.document_number,
                'first_name': p.client.first_name,
                'last_name': p.client.last_name,
                'email': p.client.email,
                'phone': p.client.phone,
                'amount': float(p.amount),
                'purchase_date': p.purchase_date,
            })

        df = pd.DataFrame(rows)

        # Agrupamos por cliente y calculamos total del último mes
        grouped = (
            df.groupby(
                ['client_id', 'document_type', 'document_number',
                 'first_name', 'last_name', 'email', 'phone'],
                as_index=False
            )['amount']
            .sum()
            .rename(columns={'amount': 'total_last_month'})
        )

        # Filtramos clientes con total > 5'000.000
        threshold = 5_000_000
        loyal_clients = grouped[grouped['total_last_month'] > threshold]

        if loyal_clients.empty:
            return Response(
                {"detail": "No hay clientes que superen el monto mínimo para fidelización."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generamos Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            loyal_clients.to_excel(
                writer,
                index=False,
                sheet_name='Clientes_fidelizacion'
            )

        output.seek(0)

        filename = f"reporte_fidelizacion_{today.isoformat()}.xlsx"

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

